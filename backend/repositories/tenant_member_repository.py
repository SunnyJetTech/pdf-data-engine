from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.models.tenant_member import TenantMember
from repositories.base_repository import BaseRepository

class TenantMemberRepository(BaseRepository[TenantMember]):

    def __init__(self, db):
        super().__init__(db=db, model=TenantMember)

    def by_id(self, member_id: uuid.UUID) -> TenantMember | None:
        stmt = select(TenantMember).where(TenantMember.id == member_id)

        return self.db.scalar_one_or_none(stmt)

    def membership(self, *, tenant_id: uuid.UUID, user_id: uuid.UUID) -> TenantMember | None:
        stmt = (
            select(TenantMember)
            .options( joinedload(TenantMember.role))
            .where( TenantMember.tenant_id == tenant_id, TenantMember.user_id == user_id,)
        )

        return self.db.scalar_one_or_none(stmt)

    def tenant_members(self, tenant_id: uuid.UUID) -> list[TenantMember]:
        stmt = (
            select(TenantMember)
            .options( joinedload(TenantMember.user), joinedload(TenantMember.role))
            .where( TenantMember.tenant_id == tenant_id)
            .order_by(TenantMember.created_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def user_memberships(self, user_id: uuid.UUID) -> list[TenantMember]:
        stmt = (
            select(TenantMember)
            .options( joinedload(TenantMember.tenant), joinedload(TenantMember.role))
            .where( TenantMember.user_id == user_id)
            .order_by(TenantMember.created_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def by_role(self, *, tenant_id: uuid.UUID, role_id: uuid.UUID) -> list[TenantMember]:
        stmt = (
            select(TenantMember)
            .options( joinedload(TenantMember.user))
            .where( TenantMember.tenant_id == tenant_id, TenantMember.role_id == role_id,)
            .order_by(TenantMember.created_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def is_member(self, *, tenant_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        
        return self.exists(tenant_id=tenant_id, user_id=user_id)

    def remove_member( self, *, tenant_id: uuid.UUID, user_id: uuid.UUID) -> None:
        member = self.membership(tenant_id=tenant_id, user_id=user_id)

        if member is not None:
            self.delete(member)