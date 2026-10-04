from __future__ import annotations
from sqlalchemy import select
from core.models.permission import Permission
from repositories.base_repository import BaseRepository

class PermissionRepository(BaseRepository[Permission]):

    def __init__(self, db):
        super().__init__(db=db, model=Permission)

    def by_name(self, name: str) -> Permission | None:
        stmt = select(Permission).where(Permission.name == name)

        return self.db.scalar(stmt)

    def by_resource(self, resource: str) -> list[Permission]:
        stmt = (select(Permission).where(Permission.resource == resource).order_by(Permission.action.asc()))

        return list(self.db.scalars(stmt).all())

    def by_action(self, action: str) -> list[Permission]:
        stmt = (select(Permission).where(Permission.action == action).order_by(Permission.resource.asc()))

        return list(self.db.scalars(stmt).all())

    def system_permissions(self) -> list[Permission]:
        stmt = (select(Permission).where(Permission.is_system.is_(True)).order_by(Permission.resource.asc(), Permission.action.asc()))

        return list(self.db.scalars(stmt).all())

    def custom_permissions(self) -> list[Permission]:
        stmt = (select(Permission).where(Permission.is_system.is_(False)).order_by(Permission.resource.asc(), Permission.action.asc()))

        return list(self.db.scalars(stmt).all())