from __future__ import annotations
from uuid import UUID
from sqlalchemy import desc, select, delete, func
from sqlalchemy.orm import Session, joinedload
from core.models.search import SavedSearch
from repositories.base_repository import BaseRepository

class SavedSearchRepository(BaseRepository[SavedSearch]):

    def __init__(self, db: Session):
        super().__init__(db, SavedSearch)

    def by_user(self, user_id: UUID) -> list[SavedSearch]:
        stmt = select(SavedSearch).where(SavedSearch.user_id == user_id).order_by(desc(SavedSearch.created_at))

        return list(self.db.scalars(stmt).all())

    def by_dataset(self, dataset_id: UUID) -> list[SavedSearch]:
        stmt = (
            select(SavedSearch)
            .options(joinedload(SavedSearch.user),)
            .where(SavedSearch.dataset_id == dataset_id)
            .order_by(SavedSearch.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    def by_name(self, *, user_id: UUID, name: str) -> SavedSearch | None:
        stmt = select(SavedSearch).where(SavedSearch.user_id == user_id, SavedSearch.name == name,).limit(1)

        return self.db.scalar(stmt)

    def by_id(self, search_id: UUID) -> SavedSearch | None:
        stmt = select(SavedSearch).options(joinedload(SavedSearch.dataset), joinedload(SavedSearch.user)).where(SavedSearch.id == search_id)

        return self.db.scalar(stmt)
    
    def exists_name(self, *, user_id: UUID, name: str) -> bool:
        stmt = select(SavedSearch.id).where(SavedSearch.user_id == user_id, SavedSearch.name == name)

        return self.db.scalar(stmt) is not None
    
    def rename(self, *, saved_search: SavedSearch, name: str) -> SavedSearch:
        saved_search.name = name

        return saved_search
    
    def count_by_user(self, *, user_id: UUID) -> int:
        stmt = select(func.count()).select_from(SavedSearch).where(SavedSearch.user_id == user_id)

        return self.db.scalar(stmt) or 0
    
    def delete_by_dataset(self, *, dataset_id: UUID) -> None:
        stmt = delete(SavedSearch).where(SavedSearch.dataset_id == dataset_id)

        self.db.execute(stmt)
