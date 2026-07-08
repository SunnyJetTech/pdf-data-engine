from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models import User
from core.responses_builder import success
from db.database import get_db
from services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["PAYMENTS"],
)

@router.post("/initialize")
def initialize_payment(amount: int, plan_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    payment = PaymentService.initialize(db=db, user=current_user, amount=amount, plan_name=plan_name)

    return success(
        data=payment,
        message="Payment initialized successfully.",
    )


@router.get("/verify/{reference}")
def verify_payment(reference: str, db: Session = Depends(get_db)):
    payment = PaymentService.verify(db=db, reference=reference)

    return success(
        data=payment,
        message="Payment verified successfully.",
    )


@router.post("/webhook")
async def paystack_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()

    signature = request.headers.get(
        "x-paystack-signature",
        "",
    )

    result = await PaymentService.process_webhook(db=db, payload=payload, signature=signature)

    return success(
        data=result,
        message="Webhook processed successfully.",
    )