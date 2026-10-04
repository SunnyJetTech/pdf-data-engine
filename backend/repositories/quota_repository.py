from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.quota import Quota
from repositories.base_repository import BaseRepository

class QuotaRepository(BaseRepository[Quota]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Quota)

    def by_tenant(self, tenant_id: uuid.UUID) -> Quota | None:
        stmt = select(Quota).where(Quota.tenant_id == tenant_id)

        return self.db.scalar(stmt)

    def create_for_tenant(self, tenant_id: uuid.UUID, **limits) -> Quota:
        quota = Quota(tenant_id=tenant_id, **limits)
        self.db.add(quota)

        return quota

    def lock(self, quota: Quota) -> Quota:

        return self.update(quota, is_locked=True)

    def unlock(self, quota: Quota) -> Quota:

        return self.update(quota, is_locked=False)

    def update_limits(self, quota: Quota, **limits) -> Quota:

        return self.update(quota, **limits)

    def update_storage_limit(self, quota: Quota, storage_limit_mb: int) -> Quota:

        return self.update(quota, storage_limit_mb=storage_limit_mb)

    def reset(self, quota: Quota) -> Quota:

        return self.update(quota, reset_at=None, is_locked=False)

    def can_create_dataset(self, quota: Quota, current_usage: int) -> bool:

        return current_usage < quota.datasets_limit

    def can_upload_document(self, quota: Quota, current_usage: int,) -> bool:

        return current_usage < quota.documents_limit

    def can_search(self, quota: Quota, current_usage: int) -> bool:

        return current_usage < quota.searches_limit

    def can_export( self, quota: Quota, current_usage: int) -> bool:

        return current_usage < quota.exports_limit
    
    def can_use_ai_tokens(self, quota: Quota, current_tokens: int, additional_tokens: int = 0) -> bool:

        return (current_tokens + additional_tokens <= quota.ai_tokens_limit)