from __future__ import annotations
from datetime import datetime, UTC
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, joinedload
from core.models.subscription import Subscription
from core.constants.subscription import SubscriptionStatus
from repositories.base_repository import BaseRepository
from uuid import UUID

class SubscriptionRepository(BaseRepository[Subscription]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Subscription,)

    def by_id(self, subscription_id: int) -> Subscription | None:
        stmt = (
            select(Subscription)
            .options(joinedload(Subscription.plan), joinedload(Subscription.tenant))
            .where(Subscription.id == subscription_id)
        )

        return self.db.scalar(stmt)

    def active(self, tenant_id: UUID) -> Subscription | None:
        stmt = (
            select(Subscription)
            .options(joinedload(Subscription.plan))
            .where(Subscription.tenant_id == tenant_id, Subscription.status == SubscriptionStatus.ACTIVE)
            .order_by(desc(Subscription.expires_at))
            .limit(1)
        )

        return self.db.scalar(stmt)

    def history(self, tenant_id) -> list[Subscription]:
        stmt = (
            select(Subscription)
            .options(joinedload(Subscription.plan))
            .where(Subscription.tenant_id == tenant_id)
            .order_by(desc(Subscription.created_at))
        )

        return list(self.db.scalars(stmt).all())

    def expired(self) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.expires_at < datetime.now(UTC), Subscription.status == SubscriptionStatus.ACTIVE)

        return list(self.db.scalars(stmt).all())
    
    def deactivate(self, subscription: Subscription) -> Subscription:

        return self.update(subscription, status=SubscriptionStatus.CANCELLED)

    def activate( self, subscription: Subscription) -> Subscription:

        return self.update(subscription, status=SubscriptionStatus.ACTIVE)

    def count_active(self) -> int:
        stmt = select(func.count()).select_from(Subscription).where(Subscription.status == SubscriptionStatus.ACTIVE)

        return self.db.scalar(stmt) or 0

    def latest(self, tenant_id) -> Subscription | None:
        stmt = (
            select(Subscription)
            .where(Subscription.tenant_id == tenant_id)
            .order_by(desc(Subscription.created_at))
            .limit(1)
        )

        return self.db.scalar(stmt)

    def expiring_before(self, dt: datetime) -> list[Subscription]:
        stmt = select(Subscription).where(Subscription.expires_at <= dt, Subscription.status == SubscriptionStatus.ACTIVE)

        return list(self.db.scalars(stmt).all())

    def exists_active(self, tenant_id: UUID) -> bool:
        stmt = select(Subscription.id).where(Subscription.tenant_id == tenant_id, Subscription.status == SubscriptionStatus.ACTIVE)

        return self.db.scalar(stmt) is not None
    
    def trial(self, tenant_id: UUID) -> Subscription | None:
        stmt = (
            select(Subscription)
            .options(joinedload(Subscription.plan))
            .where(Subscription.tenant_id == tenant_id, Subscription.status == SubscriptionStatus.TRIAL)
            .order_by(desc(Subscription.expires_at))
            .limit(1)
        )

        return self.db.scalar(stmt)
    
    def cancelled(self, tenant_id: UUID) -> list[Subscription]:
        stmt = (
            select(Subscription)
            .options(joinedload(Subscription.plan))
            .where(Subscription.tenant_id == tenant_id, Subscription.status == SubscriptionStatus.CANCELLED)
            .order_by(desc(Subscription.created_at))
        )

        return list(self.db.scalars(stmt).all())
    
    def mark_expired(self, subscription: Subscription) -> Subscription:

        return self.update(subscription, status=SubscriptionStatus.EXPIRED, auto_renew=False)
    
    def renew(self, subscription: Subscription, *, starts_at: datetime, expires_at: datetime) -> Subscription:

        return self.update(subscription, status=SubscriptionStatus.ACTIVE, starts_at=starts_at, expires_at=expires_at)
    