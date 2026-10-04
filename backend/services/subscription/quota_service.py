from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models.quota import Quota
from repositories.quota_repository import QuotaRepository

class QuotaService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.quotas = QuotaRepository(db)
        
    def get(self, tenant_id: UUID) -> Quota:
        quota = self.quotas.by_tenant(tenant_id=tenant_id)

        if quota is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quota not found.")

        return quota

    def lock(self, tenant_id: UUID) -> Quota:
        quota = self.get(tenant_id)
        quota.is_locked = True
        self.db.commit()
        self.db.refresh(quota)

        return quota

    def unlock(self, tenant_id: UUID) -> Quota:
        quota = self.get(tenant_id)
        quota.is_locked = False
        self.db.commit()
        self.db.refresh(quota)

        return quota
    
    def schedule_reset(self, *, tenant_id: UUID, reset_at: datetime) -> Quota:
        quota = self.get(tenant_id)
        quota.reset_at = reset_at
        self.db.commit()
        self.db.refresh(quota)

        return quota

    def update_limits(
        self,
        *,
        tenant_id: UUID,
        datasets_limit: int | None = None,
        documents_limit: int | None = None,
        searches_limit: int | None = None,
        chat_messages_limit: int | None = None,
        exports_limit: int | None = None,
        storage_limit_mb: int | None = None,
        ai_tokens_limit: int | None = None,
    ) -> Quota:
        quota = self.get(tenant_id)
        if datasets_limit is not None:
            quota.datasets_limit = datasets_limit

        if documents_limit is not None:
            quota.documents_limit = documents_limit

        if searches_limit is not None:
            quota.searches_limit = searches_limit

        if chat_messages_limit is not None:
            quota.chat_messages_limit = chat_messages_limit

        if exports_limit is not None:
            quota.exports_limit = exports_limit

        if storage_limit_mb is not None:
            quota.storage_limit_mb = storage_limit_mb

        if ai_tokens_limit is not None:
            quota.ai_tokens_limit = ai_tokens_limit

        self.db.commit()
        self.db.refresh(quota)

        return quota

    def ensure_not_locked(self, tenant_id: UUID) -> None:
        quota = self.get(tenant_id)

        if quota.is_locked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Workspace is locked.")

    def serialize(self, quota: Quota) -> dict:

        return {
            "datasets_limit": quota.datasets_limit,
            "documents_limit": quota.documents_limit,
            "searches_limit": quota.searches_limit,
            "chat_messages_limit": quota.chat_messages_limit,
            "exports_limit": quota.exports_limit,
            "storage_limit_mb": quota.storage_limit_mb,
            "ai_tokens_limit": quota.ai_tokens_limit,
            "is_locked": quota.is_locked,
            "reset_at": quota.reset_at,
        }