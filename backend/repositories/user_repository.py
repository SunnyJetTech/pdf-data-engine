from __future__ import annotations
import uuid
from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload
from core.models.user import User
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):

    def __init__(self, db):
        super().__init__(db=db, model=User)

    def by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)

        return self.db.scalar(stmt)

    def by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)

        return self.db.scalar(stmt)

    def by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)

        return self.db.scalar(stmt)

    def by_login(self, value: str) -> User | None:
        stmt = select(User).where(or_(User.email == value, User.username == value))

        return self.db.scalar(stmt)

    def active_users(self) -> list[User]:
        stmt = select(User).where(User.is_active.is_(True)).order_by(User.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def superusers(self) -> list[User]:
        stmt = select(User).where(User.is_superuser.is_(True))

        return list(self.db.scalars(stmt).all())

    def with_memberships(self, user_id: uuid.UUID) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.tenant_memberships).joinedload("tenant"), joinedload(User.tenant_memberships).joinedload("role"))
            .where(User.id == user_id)
        )

        return self.db.scalar(stmt)

    def with_quota(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).options(joinedload(User.quota)).where(User.id == user_id)

        return self.db.scalar(stmt)

    def with_subscription(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).options(joinedload(User.subscriptions)).where(User.id == user_id)

        return self.db.scalar(stmt)

    def with_api_keys(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).options(joinedload(User.api_keys)).where(User.id == user_id)

        return self.db.scalar(stmt)

    def owned_tenants(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).options(joinedload(User.owned_tenants)).where(User.id == user_id)

        return self.db.scalar(stmt)