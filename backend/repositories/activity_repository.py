from __future__ import annotations
import uuid
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from core.models.activity import Activity
from repositories.base_repository import BaseRepository

class ActivityRepository(BaseRepository[Activity]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Activity)

    def by_id(self, activity_id: uuid.UUID) -> Activity | None:
        stmt = select(Activity).where(Activity.id == activity_id)

        return self.db.scalar(stmt)

    def by_tenant(self, tenant_id: uuid.UUID, *, limit: int = 100) -> list[Activity]:
        stmt = select(Activity).where(Activity.tenant_id == tenant_id).order_by(desc(Activity.created_at)).limit(limit)

        return list(self.db.scalars(stmt).all())

    def by_user(self, user_id: uuid.UUID, *, limit: int = 100) -> list[Activity]:
        stmt = select(Activity).where(Activity.user_id == user_id).order_by(desc(Activity.created_at)).limit(limit)

        return list(self.db.scalars(stmt).all())

    def by_document(self, document_id: uuid.UUID) -> list[Activity]:
        stmt = select(Activity).where(Activity.document_id == document_id,).order_by(desc(Activity.created_at))

        return list(self.db.scalars(stmt).all())

    def by_action(self, action: str, *, limit: int = 100) -> list[Activity]:
        stmt = select(Activity).where(    Activity.action == action,).order_by(    desc(Activity.created_at),).limit(limit)
        
        return list(self.db.scalars(stmt).all())