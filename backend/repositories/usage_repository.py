from __future__ import annotations
import uuid
from datetime import datetime, UTC
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.usage import Usage
from repositories.base_repository import BaseRepository

class UsageRepository(BaseRepository[Usage]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Usage)

    def by_tenant(self, tenant_id: uuid.UUID) -> Usage | None:
        stmt = select(Usage).where(Usage.tenant_id == tenant_id)

        return self.db.scalar(stmt)

    def create_for_tenant(self, tenant_id: uuid.UUID) -> Usage:
        usage = Usage(tenant_id=tenant_id)
        self.db.add(usage)

        return usage

    def increment_dataset(self, usage: Usage, amount: int = 1) -> Usage:
        usage.datasets_used += amount

        return usage

    def increment_documents(self, usage: Usage, amount: int = 1) -> Usage:
        usage.documents_used += amount

        return usage

    def increment_searches(self, usage: Usage, amount: int = 1) -> Usage:
        usage.searches_used += amount

        return usage

    def increment_chat_messages(self, usage: Usage, amount: int = 1) -> Usage:
        usage.chat_messages_used += amount

        return usage

    def increment_exports(self, usage: Usage, amount: int = 1) -> Usage:
        usage.exports_used += amount

        return usage

    def increase_storage(self, usage: Usage, amount_mb: int) -> Usage:
        usage.storage_used_mb += amount_mb

        return usage

    def add_tokens(self, usage: Usage, *, prompt_tokens: int, completion_tokens: int) -> Usage:
        usage.prompt_tokens_used += prompt_tokens
        usage.completion_tokens_used += completion_tokens
        usage.total_tokens_used += (prompt_tokens + completion_tokens)

        return usage

    def reset(self, usage: Usage) -> Usage:

        usage.datasets_used = 0
        usage.documents_used = 0
        usage.searches_used = 0
        usage.chat_messages_used = 0
        usage.exports_used = 0
        usage.storage_used_mb = 0
        usage.prompt_tokens_used = 0
        usage.completion_tokens_used = 0
        usage.total_tokens_used = 0
        usage.last_reset_at = datetime.now(UTC)

        return usage

    def reset_storage(self, usage: Usage) -> Usage:
        usage.storage_used_mb = 0

        return usage

    def has_usage(self, tenant_id: uuid.UUID) -> bool:
        stmt = select(Usage.id).where(Usage.tenant_id == tenant_id)

        return self.db.scalar(stmt) is not None
    
    