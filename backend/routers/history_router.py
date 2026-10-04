from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Response, status,
from core.auth import get_current_user_from_cookie
from core.dependencies.search import get_history_service
from core.models.user import User
from schemas.history.response import SearchHistoryResponse
from services.search.history_service import HistoryService

router = APIRouter(
    prefix="/history",
    tags=["Search History"],
)

@router.get("", response_model=list[SearchHistoryResponse])
async def recent_history(
    limit: int = 20,
    history: HistoryService = Depends( get_history_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    return await history.recent(user=current_user, limit=limit)

@router.get("/dataset/{dataset_id}", response_model=list[SearchHistoryResponse])
async def dataset_history(
    dataset_id: UUID,
    limit: int = 100,
    history: HistoryService = Depends(get_history_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    return await history.by_dataset(dataset_id=dataset_id, user=current_user, limit=limit)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    history: HistoryService = Depends(get_history_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    await history.clear(user=current_user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)