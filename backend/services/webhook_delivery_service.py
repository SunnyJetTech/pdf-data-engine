from __future__ import annotations
from datetime import datetime, timedelta, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models.webhook import Webhook
from core.models.webhook_delivery import WebhookDelivery
from repositories.webhook_delivery_repository import WebhookDeliveryRepository

class WebhookDeliveryService:

    def __init__(self, db: Session) -> None:    
        self.db = db
        self.deliveries = WebhookDeliveryRepository(db)

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    def by_id(self, delivery_id: UUID) -> WebhookDelivery:
        delivery = self.deliveries.by_id(delivery_id)

        if delivery is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook delivery not found.")

        return delivery

    def history(self, webhook_id: UUID, *, limit: int = 100) -> list[WebhookDelivery]:
        return self.deliveries.by_webhook(webhook_id, limit=limit)

    def latest(self, webhook_id: UUID) -> WebhookDelivery | None:
        return self.deliveries.latest(webhook_id)

    def failed(self, webhook_id: UUID) -> list[WebhookDelivery]:
        return self.deliveries.failed(webhook_id)

    def successful(self, webhook_id: UUID) -> list[WebhookDelivery]:
        return self.deliveries.successful(webhook_id)

    def queue(self, *, webhook: Webhook, event: str, payload: dict) -> WebhookDelivery:
        delivery = WebhookDelivery(webhook_id=webhook.id, event=event, payload=payload, attempt=1, success=False)

        self.deliveries.add(delivery)
        self.db.flush()

        return delivery

    def schedule_retry(self, delivery: WebhookDelivery, *, retry_count: int) -> WebhookDelivery:
        if delivery.success:
            return delivery

        if delivery.attempt >= retry_count:
            delivery.next_retry_at = None
            self.db.flush()
            return delivery

        self.deliveries.increment_attempt(delivery)
        delay_seconds = min(5 ** delivery.attempt, 3600)

        delivery.next_retry_at = (self._now() + timedelta(seconds=delay_seconds))

        self.db.flush()

        return delivery

    def mark_success(self, *, delivery: WebhookDelivery, http_status: int, response_body: str | None, duration_ms: int) -> WebhookDelivery:
        now = self._now()

        self.deliveries.mark_success(
            delivery,
            http_status=http_status,
            response_body=response_body,
            duration_ms=duration_ms,
            delivered_at=now,
        )

        self.db.flush()

        return delivery

    def mark_failed(
        self,
        *,
        delivery: WebhookDelivery,
        http_status: int | None,
        response_body: str | None,
        duration_ms: int | None,
        error_message: str | None,
        next_retry_at: datetime | None,
    ) -> WebhookDelivery:
        self.deliveries.mark_failed(
            delivery,
            http_status=http_status,
            response_body=response_body,
            duration_ms=duration_ms,
            error_message=error_message,
            next_retry_at=next_retry_at,
        )

        self.db.flush()

        return delivery

    def next_retry(self, webhook_id: UUID) -> WebhookDelivery | None:
        return self.deliveries.next_retry(webhook_id=webhook_id, now=self._now())