from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.webhook import Webhook
from repositories.base_repository import BaseRepository

class WebhookRepository(BaseRepository[Webhook]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Webhook)

    def by_id(self, webhook_id: uuid.UUID) -> Webhook | None:
        stmt = select(Webhook).where(Webhook.id == webhook_id)
        return self.db.scalar(stmt)

    def by_tenant(self, tenant_id: uuid.UUID) -> list[Webhook]:
        stmt = select(Webhook).where(Webhook.tenant_id == tenant_id).order_by(Webhook.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def active(self, tenant_id: uuid.UUID) -> list[Webhook]:
        stmt = select(Webhook).where(Webhook.tenant_id == tenant_id, Webhook.active.is_(True)).order_by(Webhook.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def inactive(self, tenant_id: uuid.UUID) -> list[Webhook]:
        stmt = select(Webhook).where( Webhook.tenant_id == tenant_id, Webhook.active.is_(False)).order_by(Webhook.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def by_name(self, *, tenant_id: uuid.UUID, name: str) -> Webhook | None:
        stmt = select(Webhook).where(Webhook.tenant_id == tenant_id, Webhook.name == name)

        return self.db.scalar(stmt)

    def enable(self, webhook: Webhook) -> Webhook:
        return self.update(webhook, active=True)

    def disable(self, webhook: Webhook) -> Webhook:
        return self.update(webhook, active=False)

    def increment_failure(self, webhook: Webhook) -> Webhook:
        webhook.failure_count += 1
        return webhook

    def reset_failures(self, webhook: Webhook) -> Webhook:
        return self.update(webhook, failure_count=0)

    def update_last_delivery(self, webhook: Webhook, delivered_at) -> Webhook:
        return self.update(webhook, last_delivery_at=delivered_at)

    def exists_name(self, *, tenant_id: uuid.UUID, name: str) -> bool:
        stmt = select(Webhook.id).where(Webhook.tenant_id == tenant_id, Webhook.name == name)

        return self.db.scalar(stmt) is not None