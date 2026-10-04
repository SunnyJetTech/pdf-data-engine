from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from core.models.api_key import APIKey
from repositories.base_repository import BaseRepository

class APIKeyRepository(BaseRepository[APIKey]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=APIKey)

    def by_id(self, api_key_id: uuid.UUID) -> APIKey | None:
        stmt = select(APIKey).where(APIKey.id == api_key_id)
        return self.db.scalar(stmt)

    def by_hash(self, key_hash: str) -> APIKey | None:
        stmt = (
            select(APIKey)
            .options(joinedload(APIKey.tenant))
            .where(APIKey.key_hash == key_hash, APIKey.is_active.is_(True), APIKey.revoked_at.is_(None))
        )

        return self.db.scalar(stmt)

    def by_prefix(self, prefix: str) -> list[APIKey]:
        stmt = select(APIKey).where(APIKey.key_prefix == prefix)

        return list(self.db.scalars(stmt).all())

    def user_keys(self, user_id: uuid.UUID) -> list[APIKey]:
        stmt = select(APIKey).where(APIKey.created_by == user_id).order_by(APIKey.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def tenant_keys(self, tenant_id: uuid.UUID) -> list[APIKey]:
        stmt = select(APIKey).where(APIKey.tenant_id == tenant_id).order_by(APIKey.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def active_keys(self, tenant_id: uuid.UUID) -> list[APIKey]:
        stmt = (
            select(APIKey)
            .where(APIKey.tenant_id == tenant_id,APIKey.is_active.is_(True),APIKey.revoked_at.is_(None))
            .order_by(APIKey.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    def revoke(self, api_key: APIKey, *, revoked_at: datetime) -> APIKey:
        api_key.is_active = False
        api_key.revoked_at = revoked_at
        
        return api_key

    def activate(self, api_key: APIKey) -> APIKey:
        api_key.is_active = True
        return api_key

    def touch(self, api_key: APIKey, *, used_at: datetime) -> APIKey:
        api_key.last_used_at = used_at
        return api_key