from __future__ import annotations
from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.refresh_token import RefreshToken
from repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=RefreshToken)

    def by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)

        return self.db.scalar(stmt)

    def active_for_user(self, user_id: UUID) -> list[RefreshToken]:
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))

        return list(self.db.scalars(stmt).all())

    def revoke(self, token: RefreshToken) -> RefreshToken:

        return self.update(token, revoked_at=datetime.utcnow())

    def revoke_family( self, family_id: str) -> None:
        tokens = list(self.db.scalars(select(RefreshToken).where(RefreshToken.family_id == family_id)))
        now = datetime.utcnow()

        for token in tokens:
            token.revoked_at = now

    def revoke_user(self, user_id: UUID) -> None:
        tokens = self.active_for_user(user_id)
        now = datetime.utcnow()

        for token in tokens:
            token.revoked_at = now