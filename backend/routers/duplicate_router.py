from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from core.auth import get_current_user_from_cookie
from core.dependencies.dataset import get_dataset_service
from core.dependencies.search import get_duplicate_service
from core.models.user import User
from schemas.duplicate.response import DuplicateResponse
from backend.services.dataset_service import DatasetService
from services.search.duplicate_service import DuplicateService

router = APIRouter(
    prefix="/duplicates",
    tags=["Duplicates"],
)

@router.get("/dataset/{dataset_id}", response_model=DuplicateResponse, status_code=status.HTTP_200_OK)
async def find_duplicates(
    dataset_id: UUID,
    column: str = Query(...),
    duplicates: DuplicateService = Depends(get_duplicate_service),
    datasets: DatasetService = Depends(get_dataset_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    dataset = await datasets.get(dataset_id=dataset_id, user=current_user)

    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

    return await duplicates.find_dataset_duplicates(dataset=dataset, column=column, user=current_user)