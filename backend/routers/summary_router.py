from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,status
from core.auth import get_current_user_from_cookie
from core.dependencies.dataset import get_dataset_service
from core.dependencies.search import get_summary_service
from core.models.user import User
from schemas.summary.response import SummaryResponse
from backend.services.dataset_service import DatasetService
from services.summary.summary_service import SummaryService

router = APIRouter(
    prefix="/summary",
    tags=["Summary"],
)

@router.get("/dataset/{dataset_id}", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
async def dataset_summary(
    dataset_id: UUID,
    summaries: SummaryService = Depends(get_summary_service),
    datasets: DatasetService = Depends(get_dataset_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    dataset = await datasets.get(dataset_id=dataset_id, user=current_user)

    if dataset is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

    return await summaries.generate_dataset(dataset=dataset, user=current_user)