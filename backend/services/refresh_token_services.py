from __future__ import annotations
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.config import settings
from core.models.refresh_token import RefreshToken
from repositories.refresh_token_repository import RefreshTokenRepository

class RefreshTokenService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = RefreshTokenRepository(db)

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_family_id() -> str:
        return uuid.uuid4().hex

    def create(self, *, user_id: uuid.UUID, ip_address: str | None, user_agent: str | None) -> str:
        plaintext = self.generate_token()

        token = RefreshToken(
            user_id=user_id,
            family_id=self.generate_family_id(),
            token_hash=self.hash_token(plaintext),
            expires_at=(datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)),
            created_ip=ip_address,
            user_agent=user_agent,
        )

        self.db.add(token)
        self.db.flush()

        return plaintext

    def verify(self, *, refresh_token: str) -> RefreshToken:
        token_hash = self.hash_token(refresh_token)
        token = self.repository.by_hash(token_hash)

        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")

        now = datetime.now(timezone.utc)

        if token.expires_at <= now:
            self.repository.revoke(token)

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired.")

        if token.revoked_at is not None:
            self.repository.revoke_family(token.family_id)
            token.reuse_detected = True

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token reuse detected.")

        token.last_used_at = now

        return token

    def rotate(self, *, refresh_token: str) -> tuple[RefreshToken, str]:
        current = self.verify(refresh_token=refresh_token)
        new_plaintext = self.generate_token()

        new_token = RefreshToken(
            user_id=current.user_id,
            family_id=current.family_id,
            token_hash=self.hash_token(new_plaintext),
            expires_at=(datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)),
            created_ip=current.created_ip,
            user_agent=current.user_agent,
        )

        self.db.add(new_token)
        self.db.flush()

        current.revoked_at = datetime.now(timezone.utc)
        current.replaced_by = new_token.id

        return new_token, new_plaintext

    def revoke(self, *, refresh_token: str) -> None:
        token = self.verify(refresh_token=refresh_token)

        self.repository.revoke(token)

    def revoke_user_sessions(self, *, user_id: uuid.UUID) -> None:
        self.repository.revoke_user(user_id)

    def revoke_family(self, *, family_id: str) -> None:
        self.repository.revoke_family(family_id)