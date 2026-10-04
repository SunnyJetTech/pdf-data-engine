from __future__ import annotations
from uuid import UUID
from sqlalchemy import delete, func, select
from sqlalchemy.orm import joinedload
from repositories.base_repository import BaseRepository
from core.models.search import SearchHistory

class SearchHistoryRepository(BaseRepository[SearchHistory]):

    def __init__(self, db):
        super().__init__(db=db, model=SearchHistory)

    def by_id(self, history_id: UUID) -> SearchHistory | None:
        stmt = (
            select(SearchHistory)
            .options(joinedload(SearchHistory.dataset), joinedload(SearchHistory.user))
            .where(SearchHistory.id == history_id)
        )

        return self.db.scalar(stmt)
    
    def by_user(self, *, user_id: UUID) -> list[SearchHistory]:
        stmt = select(SearchHistory).where(SearchHistory.user_id == user_id).order_by(SearchHistory.created_at.desc())

        return list(self.db.scalars(stmt).all())

    def recent(self, *, user_id: UUID, limit: int = 20) -> list[SearchHistory]:
        stmt = select(SearchHistory).where(SearchHistory.user_id == user_id).order_by(SearchHistory.created_at.desc()).limit(limit)

        return list(self.db.scalars(stmt).all())

    def by_dataset(self, *, dataset_id: UUID, limit: int = 100) -> list[SearchHistory]:
        stmt = (
            select(SearchHistory)
            .options(joinedload(SearchHistory.user))
            .where(SearchHistory.dataset_id == dataset_id)
            .order_by(SearchHistory.created_at.desc())
            .limit(limit)
        )
        
        return list(self.db.scalars(stmt).all())

    def delete_by_user(self, *, user_id: UUID) -> None:
        stmt = delete(SearchHistory).where(SearchHistory.user_id == user_id)

        self.db.execute(stmt)
        
    def count_by_dataset(self, dataset_id: UUID) -> int:
        stmt = select(func.count()).select_from(SearchHistory).where(SearchHistory.dataset_id == dataset_id)

        return self.db.scalar(stmt) or 0
    
    def count_by_user(self, user_id: UUID) -> int:
        stmt = select(func.count()).select_from(SearchHistory).where(SearchHistory.user_id == user_id)

        return self.db.scalar(stmt) or 0
    
    def delete_by_dataset(self, *, dataset_id: UUID) -> None:
        stmt = delete(SearchHistory).where(SearchHistory.dataset_id == dataset_id)

        self.db.execute(stmt)
    
    def last_search(self, *, user_id: UUID) -> SearchHistory | None:
        stmt = select(SearchHistory).where(SearchHistory.user_id == user_id).order_by(SearchHistory.created_at.desc()).limit(1)

        return self.db.scalar(stmt)
    
    