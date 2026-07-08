from __future__ import annotations
import json
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.models import Payment, User
from services.activity_service import ActivityService
from services.mail_service import MailService
from services.paystack_service import PaystackService
from services.subscription_service import SubscriptionService

class PaymentService:

    @classmethod
    def initialize(cls, *, db: Session, user: User, amount: int, plan_name: str) -> dict:

        reference = str(uuid.uuid4())

        payment = Payment(user_id=user.id, amount=amount, reference=reference, status="pending")

        db.add(payment)
        db.commit()
        db.refresh(payment)

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.PAYMENT_INITIALIZED)

        return PaystackService.initialize_payment(
            email=user.email,
            amount=amount,
            reference=reference,
            metadata={
                "user_id": user.id,
                "plan_name": plan_name,
            },
        )

    @classmethod
    def verify(cls, *, db: Session, reference: str) -> dict:

        payment = db.query(Payment).filter(Payment.reference == reference).first()

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found.")

        result = PaystackService.verify_payment(reference)

        if (result["status"] and result["data"]["status"] == "success"):

            if payment.status != "success":

                payment.status = "success"

                SubscriptionService.activate(db=db, user_id=payment.user_id, plan_name="Premium")

                ActivityService.log(db=db, user_id=payment.user_id, action=ActivityAction.PAYMENT_SUCCESS)

                db.commit()

            return {
                "verified": True,
                "reference": payment.reference,
            }

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment verification failed.",
        )

    @classmethod
    async def process_webhook(cls, *, db: Session, payload: bytes, signature: str) -> dict:

        if not PaystackService.verify_signature(payload=payload, signature=signature,):
            raise HTTPException(
                status_code=400,
                detail="Invalid Paystack signature.",
            )

        event = json.loads(payload)

        if event.get("event") != "charge.success":
            return {
                "status": "ignored",
            }

        payment_data = event["data"]

        reference = payment_data["reference"]

        payment = db.query(Payment).filter(Payment.reference == reference).first()

        if not payment:
            return {
                "status": "payment_not_found",
            }

        if payment.status == "success":
            return {
                "status": "already_processed",
            }

        payment.status = "success"

        SubscriptionService.activate(db=db, user_id=payment.user_id, plan_name="Premium")

        ActivityService.log(db=db, user_id=payment.user_id, action=ActivityAction.PAYMENT_SUCCESS)

        db.commit()

        return {
            "status": "success",
        }