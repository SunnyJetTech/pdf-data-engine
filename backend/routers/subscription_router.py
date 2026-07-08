from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from core.auth import get_current_user_from_cookie
from core.models import User
from core.responses_builder import success, failed
from schema.response_schema import APIResponse
from services.subscription_service import SubscriptionService
from services.paystack_service import PaystackService

router = APIRouter(
    prefix="/subscriptions",
    tags=["SUBSCRIPTIONS"],
)

@router.get("/plans", response_model=APIResponse)
def get_plans(db: Session = Depends(get_db)):
    return success(
        data=SubscriptionService.get_plans(db=db),
        message="Current pricing plans",
    )

@router.get("/me", response_model=APIResponse)
def get_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    subscription = SubscriptionService.get_active(db=db, user_id=current_user.id)

    if not subscription:
        return success(
            message="No active subscription",
            data=None,
        )

    return success(
        message="Your current subscription",
        data=SubscriptionService.serialize(subscription),
    )

@router.post("/checkout", response_model=APIResponse)
def create_checkout(plan: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    pricing = SubscriptionService.get_plan_by_name(db=db, plan_name=plan)

    if not pricing:
        return failed("Invalid pricing plan.")

    payment = PaystackService.initialize_payment(email=current_user.email, amount=pricing.amount)

    return success(
        message="Checkout initialized successfully.",
        data={
            "plan": pricing.name,
            "amount": pricing.amount,
            "authorization_url": payment["data"]["authorization_url"],
            "reference": payment["data"]["reference"],
        },
    )