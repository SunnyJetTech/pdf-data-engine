from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.subscription.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)

@router.get("/current", response_model=APIResponse)
def get_current_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SubscriptionService(db)

    subscription = service.current(current_user.current_tenant_id)

    return success(subscription, "Current subscription retrieved successfully.")

@router.get("/history", response_model=APIResponse)
def get_subscription_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SubscriptionService(db)

    history = service.history(current_user.current_tenant_id)

    return success(history, "Subscription history retrieved successfully.")

@router.get("/trial", response_model=APIResponse)
def get_trial_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SubscriptionService(db)

    trial = service.trial(current_user.current_tenant_id)

    return success(trial, "Trial subscription retrieved successfully.")

@router.get("/cancelled", response_model=APIResponse)
def get_cancelled_subscriptions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SubscriptionService(db)

    cancelled = service.cancelled(current_user.current_tenant_id)

    return success(cancelled, "Cancelled subscriptions retrieved successfully.")

@router.get("/latest", response_model=APIResponse)
def get_latest_subscription( db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SubscriptionService(db)

    subscription = service.latest(current_user.current_tenant_id)

    return success(subscription, "Latest subscription retrieved successfully.")