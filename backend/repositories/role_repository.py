from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from core.models.role import Role
from repositories.base_repository import BaseRepository
from core.models.role_permission import RolePermission

class RoleRepository(BaseRepository[Role]):

    def __init__(self, db):
        super().__init__(db=db, model=Role)

    def by_id(self, role_id: uuid.UUID) -> Role | None:
        stmt = select(Role).where(Role.id == role_id)

        return self.db.scalar(stmt)

    def by_name(self, *, name: str, tenant_id: uuid.UUID) -> Role | None:
        stmt = (select(Role).where( Role.name == name, Role.tenant_id == tenant_id))

        return self.db.scalar(stmt)

    def tenant_roles(
        self,
        tenant_id: uuid.UUID,
    ) -> list[Role]:
        stmt = (select(Role).where(Role.tenant_id == tenant_id).order_by(Role.name.asc()))

        return list(self.db.scalars(stmt).all())

    def system_roles(self, tenant_id: uuid.UUID) -> list[Role]:
        stmt = (select(Role).where(Role.tenant_id == tenant_id, Role.is_system.is_(True)).order_by(Role.name.asc()))

        return list(self.db.scalars(stmt).all())

    def available_roles(self, tenant_id: uuid.UUID) -> list[Role]:

        return self.tenant_roles(tenant_id)

    def with_permissions(self, role_id: uuid.UUID) -> Role | None:
        stmt = (select(Role).options( selectinload(Role.role_permissions).selectinload(RolePermission.permission)).where(Role.id == role_id))

        return self.db.scalar_one_or_none(stmt)

    def owner_role(self, tenant_id: uuid.UUID) -> Role | None:
        return self.by_name(name="Owner", tenant_id=tenant_id)

    def admin_role(self, tenant_id: uuid.UUID) -> Role | None:
        return self.by_name(name="Admin", tenant_id=tenant_id)

    def viewer_role(self, tenant_id: uuid.UUID) -> Role | None:
        return self.by_name(name="Viewer", tenant_id=tenant_id)