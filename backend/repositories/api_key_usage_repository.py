from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.api_key_usage import APIKeyUsage
from repositories.base_repository import BaseRepository

class APIKeyUsageRepository(BaseRepository[APIKeyUsage]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=APIKeyUsage)

    def by_api_key(self, api_key_id: uuid.UUID, *, limit: int = 100) -> list[APIKeyUsage]:
        stmt = select(APIKeyUsage).where(APIKeyUsage.api_key_id == api_key_id).order_by(APIKeyUsage.created_at.desc()).limit(limit)

        return list(self.db.scalars(stmt).all())

    def by_tenant(self, tenant_id: uuid.UUID, *, limit: int = 100) -> list[APIKeyUsage]:
        stmt = select(APIKeyUsage).where(APIKeyUsage.tenant_id == tenant_id).order_by(APIKeyUsage.created_at.desc()).limit(limit)

        return list(self.db.scalars(stmt).all())