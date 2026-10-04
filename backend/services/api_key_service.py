from __future__ import annotations
import hashlib
import secrets
from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models.api_key import APIKey
from repositories.api_key_repository import APIKeyRepository

class APIKeyService:
    PREFIX = "ds_live_"

    def __init__(self, db: Session) -> None:
        self.db = db
        self.keys = APIKeyRepository(db)

    @classmethod
    def _generate_plaintext_key(cls) -> str:
        token = secrets.token_urlsafe(32)
        return f"{cls.PREFIX}{token}"

    @staticmethod
    def _hash_key(key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    @staticmethod
    def _prefix(key: str) -> str:
        return key[:12]

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    def create( self, *, tenant_id: UUID, created_by: UUID | None, name: str, expires_at: datetime | None = None) -> tuple[APIKey, str]:
        plaintext = self._generate_plaintext_key()

        api_key = APIKey(
            tenant_id=tenant_id,
            created_by=created_by,
            name=name,
            key_prefix=self._prefix(plaintext),
            key_hash=self._hash_key(plaintext),
            expires_at=expires_at,
            is_active=True,
        )

        self.keys.add(api_key)
        self.db.flush()

        return api_key, plaintext

    def authenticate(self, *, api_key: str) -> APIKey:
        hashed = self._hash_key(api_key)

        key = self.keys.by_hash(key_hash=hashed)

        if key is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")

        now = self._now()

        if not key.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key is inactive.")

        if key.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key has been revoked.")

        if (key.expires_at is not None and key.expires_at <= now):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key has expired.")

        self.keys.touch(key, used_at=now)

        return key

    def rotate(self, *, key: APIKey) -> str:
        plaintext = self._generate_plaintext_key()

        key.key_hash = self._hash_key(plaintext)
        key.key_prefix = self._prefix(plaintext)
        key.last_used_at = None
        key.revoked_at = None
        key.is_active = True

        self.db.flush()

        return plaintext

    def revoke(self, key: APIKey) -> APIKey:
        self.keys.revoke(key, revoked_at=self._now())
        self.db.flush()

        return key

    def activate(self, key: APIKey) -> APIKey:
        if key.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A revoked API key cannot be activated. Rotate it instead.")

        self.keys.activate(key)
        self.db.flush()

        return key

    def delete(self, key: APIKey) -> None:
        self.keys.delete(key)

    def by_id(self, key_id: UUID) -> APIKey:
        key = self.keys.by_id(key_id)

        if key is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

        return key

    def by_tenant(self, tenant_id: UUID) -> list[APIKey]:
        return self.keys.tenant_keys(tenant_id=tenant_id)