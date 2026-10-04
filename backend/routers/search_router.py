from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from core.auth import get_current_user_from_cookie
from core.dependencies.search import get_search_service
from core.models.user import User
from schemas.search.request import SearchRequest
from schemas.search.response import SearchResponse
from services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

def _ensure_dataset_access(*, service: SearchService, current_user: User, dataset_id: UUID):
    dataset = service.db.get_by_id(dataset_id) if hasattr(service.db, "get_by_id") else None

    if dataset is None:
        from services.dataset_service import DatasetService

        dataset = DatasetService(service.db).get(dataset_id)

    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

    if dataset.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Dataset does not belong to your workspace.")

    return dataset

@router.post("", response_model=SearchResponse, status_code=status.HTTP_200_OK)
async def search_dataset(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    _ensure_dataset_access(service=service, current_user=current_user, dataset_id=request.dataset_id)

    return await service.search(user_id=current_user.id, dataset_id=request.dataset_id, query=request.query)

@router.get("/history", status_code=status.HTTP_200_OK)
async def search_history(
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    return service.history_for_user(user_id=current_user.id)

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_search_history(
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    service.clear_history(user_id=current_user.id)

@router.get("/saved", status_code=status.HTTP_200_OK)
async def saved_searches(
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    
    return service.saved_searches(user_id=current_user.id)

@router.post("/saved", status_code=status.HTTP_201_CREATED)
async def save_search(
    request: SearchRequest,
    name: str,
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    _ensure_dataset_access(service=service, current_user=current_user, dataset_id=request.dataset_id)

    return service.save_search(user_id=current_user.id, dataset_id=request.dataset_id, name=name, query=request.query)

@router.delete("/saved/{saved_search_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_search(
    saved_search_id: UUID,
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    
    service.delete_saved_search(search_id=saved_search_id)
