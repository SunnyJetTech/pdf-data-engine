from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core.models import Subscription, PricingPlan


class SubscriptionService:
    DEFAULT_DURATION_DAYS = 30

    @staticmethod
    def deactivate_existing(*, db: Session, user_id: int,) -> None:

        (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.is_active.is_(True),
            )
            .update(
                {"is_active": False},
                synchronize_session=False,
            )
        )

    @classmethod
    def activate(cls, *, db: Session, user_id: int, plan_name: str, duration_days: int | None = None) -> Subscription:
        duration = duration_days or cls.DEFAULT_DURATION_DAYS

        cls.deactivate_existing(db=db, user_id=user_id)

        subscription = Subscription(
            user_id=user_id,
            plan_name=plan_name,
            is_active=True,
            start_date=datetime.utcnow(),
            expiry_date=datetime.utcnow()
            + timedelta(days=duration),
        )

        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        return subscription

    @staticmethod
    def get_active(*, db: Session, user_id: int) -> Subscription | None:

        return db.query(Subscription).filter(Subscription.user_id == user_id,Subscription.is_active.is_(True),Subscription.expiry_date > datetime.utcnow()).first()

    @classmethod
    def has_active(cls, *, db: Session, user_id: int) -> bool:
        return cls.get_active(db=db, user_id=user_id) is not None

    @staticmethod
    def deactivate(*, db: Session, subscription: Subscription) -> None:

        subscription.is_active = False
        db.commit()

    @staticmethod
    def expired(subscription: Subscription) -> bool:
        return (subscription.expiry_date <= datetime.utcnow())
    

    @staticmethod
    def serialize_plan(plan: PricingPlan) -> dict:
        return {
            "id": plan.id,
            "name": plan.name,
            "price": plan.amount,
            "currency": plan.currency,
            "duration_days": plan.duration_days,
            "uploads_limit": plan.uploads_limit,
            "searches_limit": plan.searches_limit,
            "active": plan.active,
        }

    @classmethod
    def get_plans(cls, *, db: Session) -> list[dict]:

        plans = db.query(PricingPlan).filter(PricingPlan.active.is_(True)).all()

        return [cls.serialize_plan(plan) for plan in plans]

    @classmethod
    def get_plan(cls, *, db: Session, plan_id: int) -> PricingPlan | None:

        return db.query(PricingPlan).filter(PricingPlan.id == plan_id, PricingPlan.active.is_(True)).first()

    @staticmethod
    def serialize(subscription: Subscription) -> dict:
        return {
            "id": subscription.id,
            "plan_name": subscription.plan_name,
            "is_active": subscription.is_active,
            "start_date": subscription.start_date,
            "expiry_date": subscription.expiry_date,
        }
    
    @classmethod
    def get_plan_by_name(cls, *, db: Session, plan_name: str) -> PricingPlan | None:

        return (
            db.query(PricingPlan)
            .filter(
                PricingPlan.name.ilike(f"%{plan_name}%"),
                PricingPlan.active.is_(True),
            )
            .first()
        )
