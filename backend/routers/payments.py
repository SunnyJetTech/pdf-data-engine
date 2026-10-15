from __future__ import annotations
import json
from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.config import settings
from core.constants.payment import PaymentProvider
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.payment_service import PaymentService
from services.payment.paystack_service import PaystackService
from services.payment.stripe_service import StripeService
from services.payment.flutterwave_service import FlutterwaveService

router = APIRouter(
    prefix="/payments", 
    tags=["Payments"]
)

@router.get("/current/latest", response_model=APIResponse)
def get_latest_payment(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = PaymentService(db)
    payment = service.latest(current_user.current_tenant_id)

    return success(payment, "Latest payment retrieved successfully.")

@router.get("/current/history", response_model=APIResponse)
def get_payment_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = PaymentService(db)
    payments = service.history(current_user.current_tenant_id)

    return success(payments, "Payment history retrieved successfully.")

@router.get("/current/total-successful", response_model=APIResponse)
def get_total_successful_amount(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = PaymentService(db)
    total = service.total_successful_amount(current_user.current_tenant_id)

    return success({"total_successful_amount": total}, "Total successful payment amount retrieved successfully.")

@router.get("/current/successful-count", response_model=APIResponse)
def get_successful_payment_count(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = PaymentService(db)
    count = service.successful_count(current_user.current_tenant_id)

    return success({"successful_payment_count": count}, "Successful payment count retrieved successfully.")

@router.post("/initialize", response_model=APIResponse)
def initialize_payment(
    plan_id: int,
    provider: PaymentProvider,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie),
):
    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must select a tenant before making a payment.")

    service = PaymentService(db)
    result = service.initialize_payment(tenant_id=tenant_id, plan_id=plan_id, provider=provider, email=current_user.email)

    return success(result, "Payment initialized successfully.")

@router.post("/verify/{reference}", response_model=APIResponse)
def verify_payment(
    reference: str,
    provider_transaction_id: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie),
):

    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must select a tenant before verifying a payment.")

    service = PaymentService(db)
    payment = service.verify_payment(reference=reference, tenant_id=tenant_id, provider_transaction_id=provider_transaction_id)

    return success(payment, "Payment verified successfully.")

@router.post("/webhooks/paystack")
async def paystack_webhook(request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    signature = request.headers.get("x-paystack-signature")

    if not signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Paystack webhook signature.")

    provider = PaystackService()

    if not provider.verify_webhook_signature(payload=raw_body, signature=signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Paystack webhook signature.")

    try:
        event = json.loads(raw_body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload.")

    if event.get("event") == "charge.success":
        data = event.get("data") or {}
        reference = data.get("reference")

        if reference:
            service = PaymentService(db)
            payment = service.by_reference(reference)

            if payment and payment.provider == PaymentProvider.PAYSTACK:
                service.verify_payment(reference=reference, tenant_id=payment.tenant_id)

    return {"status": "success"}

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Stripe webhook signature.")

    provider = StripeService()

    if not provider.verify_webhook_signature(
        payload=raw_body,
        signature=signature,
        webhook_secret=settings.STRIPE_WEBHOOK_SECRET.get_secret_value(),
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Stripe webhook signature.")

    try:
        event = json.loads(raw_body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload.")

    event_type = event.get("type")
    data_object = ((event.get("data") or {}).get("object") or {})

    if event_type == "checkout.session.completed":
        reference = (data_object.get("client_reference_id") or (data_object.get("metadata") or {}).get("reference"))

        session_id = data_object.get("id")

        if reference:
            service = PaymentService(db)
            payment = service.by_reference(reference)

            if payment and payment.provider == PaymentProvider.STRIPE:
                service.verify_payment(reference=reference, tenant_id=payment.tenant_id, provider_transaction_id=session_id)

    return {"status": "success"}

@router.post("/webhooks/flutterwave")
async def flutterwave_webhook(request: Request, db: Session = Depends(get_db)):
    signature = request.headers.get("verif-hash")

    expected_signature = (settings.FLUTTERWAVE_WEBHOOK_SECRET.get_secret_value())

    if not signature or signature != expected_signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Flutterwave webhook signature.")

    try:
        event = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload.")

    data = event.get("data") or {}
    reference = data.get("tx_ref")
    transaction_id = data.get("id")
    event_type = event.get("event")

    if event_type == "charge.completed" and reference and transaction_id:
        service = PaymentService(db)
        payment = service.by_reference(reference)

        if payment and payment.provider == PaymentProvider.FLUTTERWAVE:
            service.verify_payment(reference=reference, tenant_id=payment.tenant_id, provider_transaction_id=str(transaction_id))

    return {"status": "success"}

@router.get("/{payment_id}", response_model=APIResponse)
def get_payment(payment_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = PaymentService(db)
    payment = service.by_id(payment_id)

    if payment.tenant_id != current_user.current_tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")

    return success(payment, "Payment retrieved successfully.")
