from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.models.search import SavedSearch, SearchHistory
from repositories.saved_search_repository import SavedSearchRepository
from repositories.search_history_repository import SearchHistoryRepository
from services.base_service import BaseService
from services.retrieval_service import RetrievalService

class SearchService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

        self.history_repository = SearchHistoryRepository(db)
        self.saved_repository = SavedSearchRepository(db)
        self.retrieval = RetrievalService()

    async def search(self, *, user_id: UUID, dataset_id: UUID, query: str, limit: int = 20) -> dict:
        self.record_history(user_id=user_id, dataset_id=dataset_id, query=query)

        results = await self.retrieval.retrieve_with_metadata(dataset_id=dataset_id, question=query, limit=limit)

        return {
            "query": query,
            "count": len(results),
            "results": results,
        }

    async def retrieve_context(self, *, dataset_id: UUID, query: str, limit: int = 8) -> list[str]:

        return await self.retrieval.retrieve_context( dataset_id=dataset_id, question=query, limit=limit)
    
    def record_history(self, *, user_id: UUID, dataset_id: UUID, query: str) -> SearchHistory:
        history = SearchHistory( user_id=user_id, dataset_id=dataset_id, query=query)

        self.history_repository.add(history)
        self.commit_refresh(history)
        self.activity.log(actor_id=user_id, action=ActivityAction.SEARCH_PERFORMED, target_type="dataset", target_id=dataset_id)

        return history

    def history_for_user(self, *, user_id: UUID) -> list[SearchHistory]:

        return self.history_repository.recent(user_id=user_id)

    def clear_history(self, *, user_id: UUID) -> int:
        deleted = self.history_repository.delete_by_user(user_id=user_id)

        self.commit()

        return deleted

    def save_search(self, *, user_id: UUID, dataset_id: UUID, name: str, query: str) -> SavedSearch:

        if self.saved_repository.by_name(user_id=user_id, name=name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Saved search already exists.")

        search = SavedSearch(user_id=user_id, dataset_id=dataset_id, name=name, query=query)

        self.saved_repository.add(search)
        self.commit_refresh(search)

        return search

    def saved_searches(self, *, user_id: UUID) -> list[SavedSearch]:

        return self.saved_repository.by_user(user_id=user_id)

    def delete_saved_search(self, *, search_id: UUID) -> None:

        search = self.saved_repository.by_id(search_id)

        if search is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved search not found.")

        self.saved_repository.delete(search)

        self.commit()