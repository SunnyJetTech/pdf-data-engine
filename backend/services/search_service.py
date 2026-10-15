from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.models.search import SavedSearch, SearchHistory
from repositories.saved_search_repository import SavedSearchRepository
from repositories.search_history_repository import SearchHistoryRepository
from services.base_service import BaseService
from services.dataset_service import DatasetService
from services.retrieval_service import RetrievalService

class SearchService(BaseService):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

        self.history_repository = SearchHistoryRepository(db)
        self.saved_repository = SavedSearchRepository(db)
        self.datasets = DatasetService(db)
        self.retrieval = RetrievalService()

    async def search(self, *, user_id: UUID, tenant_id: UUID, dataset_id: UUID, query: str, limit: int = 20) -> dict:
        self._ensure_dataset_access(dataset_id=dataset_id, tenant_id=tenant_id)

        self.record_history(user_id=user_id, dataset_id=dataset_id, query=query)
        results = await self.retrieval.retrieve_with_metadata(dataset_id=dataset_id, question=query, limit=limit)

        return {
            "query": query,
            "count": len(results),
            "results": results,
        }

    async def retrieve_context(self, *, tenant_id: UUID, dataset_id: UUID, query: str, limit: int = 8) -> list[str]:
        self._ensure_dataset_access(dataset_id=dataset_id, tenant_id=tenant_id)

        return await self.retrieval.retrieve_context(dataset_id=dataset_id, question=query, limit=limit)

    def record_history(self, *, user_id: UUID, dataset_id: UUID, query: str) -> SearchHistory:
        history = SearchHistory(user_id=user_id, dataset_id=dataset_id, query=query)

        self.history_repository.add(history)
        self.commit_refresh(history)

        self.activity.log( actor_id=user_id, action=ActivityAction.SEARCH_PERFORMED, target_type="dataset", target_id=dataset_id)

        return history

    def history_for_user(self, *, user_id: UUID) -> list[SearchHistory]:
        return self.history_repository.recent(user_id=user_id)

    def clear_history(self, *, user_id: UUID) -> int:
        deleted = self.history_repository.delete_by_user(user_id=user_id)
        self.commit()

        return deleted

    def save_search(self, *, user_id: UUID, tenant_id: UUID, dataset_id: UUID, name: str, query: str) -> SavedSearch:
        self._ensure_dataset_access(dataset_id=dataset_id, tenant_id=tenant_id)

        if self.saved_repository.by_name(user_id=user_id, name=name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Saved search already exists.")

        search = SavedSearch(user_id=user_id, dataset_id=dataset_id, name=name, query=query)
        self.saved_repository.add(search)

        return self.commit_refresh(search)

    def saved_searches(self, *, user_id: UUID) -> list[SavedSearch]:
        return self.saved_repository.by_user(user_id=user_id)

    def get_saved_search(self, *, search_id: UUID, user_id: UUID) -> SavedSearch:
        search = self.saved_repository.by_id(search_id)

        if search is None or search.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved search not found.")

        return search

    def delete_saved_search(self, *, search_id: UUID, user_id: UUID) -> None:
        search = self.get_saved_search(search_id=search_id, user_id=user_id)

        self.saved_repository.delete(search)
        self.commit()

    def _ensure_dataset_access(self, *, dataset_id: UUID, tenant_id: UUID) -> None:
        dataset = self.datasets.get(dataset_id)

        if dataset.tenant_id != tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")