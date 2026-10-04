from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models import Subscription

class AdminSubscriptionService:

    @staticmethod
    def serialize(subscription: Subscription) -> dict:
        return {
            "id": subscription.id,
            "user_id": subscription.user_id,
            "username": subscription.user.username,
            "email": subscription.user.email,
            "plan_name": subscription.plan_name,
            "is_active": subscription.is_active,
            "start_date": subscription.start_date,
            "expiry_date": subscription.expiry_date,
        }

    @classmethod
    def serialize_many(cls, subscriptions: list[Subscription]) -> list[dict]:
        return [
            cls.serialize(subscription)
            for subscription in subscriptions
        ]

    @staticmethod
    def all(db: Session) -> list[Subscription]:
        return db.query(Subscription).order_by(Subscription.start_date.desc()).all()

    @staticmethod
    def get(db: Session, subscription_id: int) -> Subscription:

        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found.",
            )

        return subscription

    @classmethod
    def cancel(cls, db: Session, subscription_id: int) -> Subscription:

        subscription = cls.get(db=db, subscription_id=subscription_id)

        subscription.is_active = False

        db.commit()
        db.refresh(subscription)

        return subscription

    @classmethod
    def activate(cls, db: Session, subscription_id: int) -> Subscription:

        subscription = cls.get(db=db, subscription_id=subscription_id)

        subscription.is_active = True

        db.commit()
        db.refresh(subscription)

        return subscription

    @classmethod
    def delete(cls, db: Session, subscription_id: int) -> None:

        subscription = cls.get(db=db, subscription_id=subscription_id)

        db.delete(subscription)
        db.commit()