from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.webhook_delivery import WebhookDelivery
from repositories.base_repository import BaseRepository

class WebhookDeliveryRepository(BaseRepository[WebhookDelivery]):

    def __init__(self, db: Session):
        super().__init__( db=db, model=WebhookDelivery)

    def by_id(self, delivery_id: uuid.UUID) -> WebhookDelivery | None:
        stmt = select(WebhookDelivery).where(WebhookDelivery.id == delivery_id)

        return self.db.scalar(stmt)

    def by_webhook(self, webhook_id: uuid.UUID, *, limit: int = 100) -> list[WebhookDelivery]:
        stmt = (
            select(WebhookDelivery)
            .where(WebhookDelivery.webhook_id == webhook_id)
            .order_by(WebhookDelivery.created_at.desc())
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def successful(self, webhook_id: uuid.UUID) -> list[WebhookDelivery]:
        stmt = (
            select(WebhookDelivery)
            .where(WebhookDelivery.webhook_id == webhook_id,WebhookDelivery.success.is_(True))
            .order_by(WebhookDelivery.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    def failed(self, webhook_id: uuid.UUID) -> list[WebhookDelivery]:
        stmt = (
            select(WebhookDelivery)
            .where(WebhookDelivery.webhook_id == webhook_id,WebhookDelivery.success.is_(False))
            .order_by(WebhookDelivery.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    def latest( self, webhook_id: uuid.UUID) -> WebhookDelivery | None:
        stmt = select(WebhookDelivery).where(WebhookDelivery.webhook_id == webhook_id).order_by(WebhookDelivery.created_at.desc()).limit(1)

        return self.db.scalar(stmt)

    def next_retry(self, *, webhook_id: uuid.UUID, now: datetime) -> WebhookDelivery | None:
        stmt = (
            select(WebhookDelivery)
            .where(
                WebhookDelivery.webhook_id == webhook_id,
                WebhookDelivery.success.is_(False),
                WebhookDelivery.next_retry_at.is_not(None),
                WebhookDelivery.next_retry_at <= now,
            )
            .order_by(WebhookDelivery.next_retry_at.asc())
            .limit(1)
        )

        return self.db.scalar(stmt)

    def increment_attempt(self, delivery: WebhookDelivery) -> WebhookDelivery:
        delivery.attempt += 1
        return delivery

    def mark_success(
        self,
        delivery: WebhookDelivery,
        *,
        http_status: int,
        response_body: str | None,
        duration_ms: int,
        delivered_at: datetime,
    ) -> WebhookDelivery:
        return self.update(
            delivery,
            success=True,
            http_status=http_status,
            response_body=response_body,
            duration_ms=duration_ms,
            delivered_at=delivered_at,
            next_retry_at=None,
            error_message=None,
        )

    def mark_failed(
        self,
        delivery: WebhookDelivery,
        *,
        http_status: int | None,
        response_body: str | None,
        duration_ms: int | None,
        error_message: str | None,
        next_retry_at: datetime | None,
    ) -> WebhookDelivery:
        return self.update(
            delivery,
            success=False,
            http_status=http_status,
            response_body=response_body,
            duration_ms=duration_ms,
            error_message=error_message,
            next_retry_at=next_retry_at,
        )