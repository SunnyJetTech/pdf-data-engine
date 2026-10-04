from __future__ import annotations
import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from auth.integration_secret import IntegrationSecretManager
from core.models.webhook import Webhook
from repositories.webhook_repository import WebhookRepository

class WebhookService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.webhooks = WebhookRepository(db)

    @staticmethod
    def _generate_secret() -> str:
        return secrets.token_urlsafe(48)

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    def by_id(self, webhook_id: UUID) -> Webhook:
        webhook = self.webhooks.by_id(webhook_id)

        if webhook is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found.")

        return webhook

    def by_tenant(self, tenant_id: UUID) -> list[Webhook]:
        return self.webhooks.by_tenant(tenant_id=tenant_id)

    def create(
        self,
        *,
        tenant_id: UUID,
        name: str,
        url: str,
        events: list[str],
        description: str | None = None,
        retry_count: int = 3,
        timeout_seconds: int = 30,
    ) -> tuple[Webhook, str]:
        if self.webhooks.exists_name(tenant_id=tenant_id, name=name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A webhook with this name already exists.")

        plaintext_secret = self._generate_secret()

        webhook = Webhook(
            tenant_id=tenant_id,
            name=name,
            url=url,
            secret=IntegrationSecretManager.encrypt(plaintext_secret),
            events=events,
            active=True,
            description=description,
            retry_count=retry_count,
            timeout_seconds=timeout_seconds,
        )

        self.webhooks.add(webhook)
        self.db.flush()

        return webhook, plaintext_secret

    def update(
        self,
        *,
        webhook: Webhook,
        name: str | None = None,
        url: str | None = None,
        events: list[str] | None = None,
        description: str | None = None,
        retry_count: int | None = None,
        timeout_seconds: int | None = None,
    ) -> Webhook:
        if name is not None:
            webhook.name = name

        if url is not None:
            webhook.url = url

        if events is not None:
            webhook.events = events

        if description is not None:
            webhook.description = description

        if retry_count is not None:
            webhook.retry_count = retry_count

        if timeout_seconds is not None:
            webhook.timeout_seconds = timeout_seconds

        self.db.flush()

        return webhook

    def rotate_secret(self, webhook: Webhook) -> tuple[Webhook, str]:
        plaintext_secret = self._generate_secret()
        webhook.secret = (IntegrationSecretManager.encrypt(plaintext_secret))

        self.db.flush()

        return webhook, plaintext_secret

    def activate(self, webhook: Webhook) -> Webhook:
        self.webhooks.enable(webhook)
        self.db.flush()
        
        return webhook

    def deactivate(self, webhook: Webhook) -> Webhook:
        self.webhooks.disable(webhook)
        self.db.flush()
        
        return webhook

    def delete(self, webhook: Webhook) -> None:
        self.webhooks.delete(webhook)

    @staticmethod
    def decrypt_secret(webhook: Webhook) -> str:
        return IntegrationSecretManager.decrypt(webhook.secret)

    @classmethod
    def sign(cls, *, payload: bytes, secret: str, timestamp: int) -> str:
        message = (f"{timestamp}.".encode("utf-8") + payload)

        return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()

    @classmethod
    def verify_signature(cls, *, payload: bytes, secret: str, timestamp: int, signature: str, tolerance_seconds: int = 300) -> bool:
        now = int(datetime.now(timezone.utc).timestamp())

        if abs(now - timestamp) > tolerance_seconds:
            return False

        expected = cls.sign( payload=payload, secret=secret, timestamp=timestamp)

        return hmac.compare_digest( expected, signature)