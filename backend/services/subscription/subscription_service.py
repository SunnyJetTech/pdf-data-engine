from __future__ import annotations
from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.subscription import SubscriptionStatus
from core.models.pricing_plan import PricingPlan
from core.models.subscription import Subscription
from repositories.subscription_repository import SubscriptionRepository

class SubscriptionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.subscriptions = SubscriptionRepository(db)

    def current(self, tenant_id: UUID) -> Subscription:
        subscription = self.subscriptions.active(tenant_id)

        if subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active subscription not found.")

        return subscription

    def by_id(self, subscription_id: UUID) -> Subscription:
        subscription = self.subscriptions.by_id(subscription_id)

        if subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found.")

        return subscription

    def latest(self, tenant_id: UUID) -> Subscription | None:
        return self.subscriptions.latest(tenant_id)

    def history(self, tenant_id: UUID) -> list[Subscription]:
        return self.subscriptions.history(tenant_id)

    def trial(self, tenant_id: UUID) -> Subscription | None:
        return self.subscriptions.trial(tenant_id)

    def cancelled(self, tenant_id: UUID) -> list[Subscription]:
        return self.subscriptions.cancelled(tenant_id)

    def subscribe(self, *, tenant_id: UUID, plan: PricingPlan, auto_renew: bool = True) -> Subscription:

        if self.subscriptions.exists_active(tenant_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tenant already has an active subscription.")

        now = datetime.utcnow()

        subscription = Subscription(
            tenant_id=tenant_id,
            plan_id=plan.id,
            status=SubscriptionStatus.ACTIVE,
            starts_at=now,
            expires_at=now + timedelta(days=plan.duration_days),
            auto_renew=auto_renew,
        )

        self.subscriptions.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)

        return subscription

    def change_plan(self, *, subscription: Subscription, plan: PricingPlan) -> Subscription:
        now = datetime.utcnow()
        
        self.subscriptions.update(subscription, plan_id=plan.id, starts_at=now, expires_at=now + timedelta(days=plan.duration_days))
        self.db.commit()
        self.db.refresh(subscription)

        return subscription

    def renew(self, subscription: Subscription) -> Subscription:
        starts_at = subscription.expires_at
        expires_at = (starts_at + timedelta(days=subscription.plan.duration_days))

        self.subscriptions.renew(subscription, starts_at=starts_at, expires_at=expires_at)
        self.db.commit()
        self.db.refresh(subscription)

        return subscription

    def expire(self, subscription: Subscription) -> Subscription:
        self.subscriptions.mark_expired(subscription)

        self.db.commit()
        self.db.refresh(subscription)

        return subscription

    def cancel(self, subscription: Subscription) -> Subscription:
        self.subscriptions.deactivate(subscription)
        self.db.commit()
        self.db.refresh(subscription)

        return subscription

    def activate(self, subscription: Subscription) -> Subscription:
        self.subscriptions.activate(subscription)
        self.db.commit()
        self.db.refresh(subscription)

        return subscription