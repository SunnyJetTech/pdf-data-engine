from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models.usage import Usage
from repositories.quota_repository import QuotaRepository
from repositories.usage_repository import UsageRepository

class UsageService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.usage = UsageRepository(db)
        self.quotas = QuotaRepository(db)

    def get(self, tenant_id: UUID) -> Usage:
        usage = self.usage.by_tenant(tenant_id=tenant_id)

        if usage is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usage not found.")

        return usage

    def can_create_dataset(self, tenant_id: UUID) -> bool:
        usage = self.get(tenant_id)
        quota = self.quotas.by_tenant(tenant_id)

        return usage.datasets_used < quota.datasets_limit

    def can_upload_document(self, tenant_id: UUID) -> bool:
        usage = self.get(tenant_id)
        quota = self.quotas.by_tenant(tenant_id)

        return usage.documents_used < quota.documents_limit

    def can_search(self, tenant_id: UUID) -> bool:
        usage = self.get(tenant_id)
        quota = self.quotas.by_tenant(tenant_id)

        return usage.searches_used < quota.searches_limit

    def can_chat(self, tenant_id: UUID) -> bool:
        usage = self.get(tenant_id)
        quota = self.quotas.by_tenant(tenant_id)

        return usage.chat_messages_used < quota.chat_messages_limit

    def can_export(self, tenant_id: UUID) -> bool:
        usage = self.get(tenant_id)
        quota = self.quotas.by_tenant(tenant_id)

        return usage.exports_used < quota.exports_limit

    def can_use_ai(self, tenant_id: UUID, tokens: int) -> bool:
        usage = self.get(tenant_id)
        quota = self.quotas.by_tenant(tenant_id)

        return (usage.total_tokens_used + tokens <= quota.ai_tokens_limit)

    def record_dataset(self, tenant_id: UUID) -> None:
        self.get(tenant_id).datasets_used += 1

    def record_document(self, tenant_id: UUID) -> None:
        self.get(tenant_id).documents_used += 1

    def record_search(self, tenant_id: UUID) -> None:
        self.get(tenant_id).searches_used += 1

    def record_chat_message(self, tenant_id: UUID) -> None:
        self.get(tenant_id).chat_messages_used += 1

    def record_export(self, tenant_id: UUID) -> None:
        self.get(tenant_id).exports_used += 1

    def record_storage(self, tenant_id: UUID, megabytes: int) -> None:
        self.get(tenant_id).storage_used_mb += megabytes

    def record_ai_usage( self, tenant_id: UUID, *, prompt_tokens: int, completion_tokens: int) -> None:
        usage = self.get(tenant_id)

        usage.prompt_tokens_used += prompt_tokens
        usage.completion_tokens_used += completion_tokens
        usage.total_tokens_used += (prompt_tokens + completion_tokens)

    def reset(self, tenant_id: UUID) -> Usage:
        usage = self.get(tenant_id)

        usage.datasets_used = 0
        usage.documents_used = 0
        usage.searches_used = 0
        usage.chat_messages_used = 0
        usage.exports_used = 0
        usage.storage_used_mb = 0
        usage.prompt_tokens_used = 0
        usage.completion_tokens_used = 0
        usage.total_tokens_used = 0
        usage.last_reset_at = datetime.now(timezone.utc)

        return usage