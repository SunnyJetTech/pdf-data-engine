from __future__ import annotations
import uuid
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload
from core.models.role_permission import RolePermission
from repositories.base_repository import BaseRepository

class RolePermissionRepository(BaseRepository[RolePermission]):

    def __init__(self, db):
        super().__init__(db=db, model=RolePermission)

    def by_role(self, role_id: uuid.UUID) -> list[RolePermission]:
        stmt = (select(RolePermission).options(joinedload(RolePermission.permission)).where(RolePermission.role_id == role_id))

        return list(self.db.scalars(stmt).all())

    def by_permission(self, permission_id: uuid.UUID) -> list[RolePermission]:
        stmt = (select(RolePermission).options(joinedload(RolePermission.role)).where(RolePermission.permission_id == permission_id))

        return list(self.db.scalars(stmt).all())

    def assignment_exists(self, *, role_id: uuid.UUID, permission_id: uuid.UUID) -> bool:
        stmt = (select(RolePermission).where(RolePermission.role_id == role_id, RolePermission.permission_id == permission_id))

        return self.db.scalar(stmt) is not None

    def assign( self, *, role_id: uuid.UUID, permission_id: uuid.UUID) -> RolePermission:
        assignment = RolePermission( role_id=role_id, permission_id=permission_id)
        self.db.add(assignment)

        return assignment

    def revoke(self, *, role_id: uuid.UUID, permission_id: uuid.UUID) -> None:
        stmt = delete(RolePermission).where(RolePermission.role_id == role_id, RolePermission.permission_id == permission_id,)

        self.db.execute(stmt)

    def revoke_all(self, role_id: uuid.UUID) -> None:
        stmt = delete(RolePermission).where(RolePermission.role_id == role_id)

        self.db.execute(stmt)