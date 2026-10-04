from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from core.auth import get_current_user_from_cookie
from core.dependencies.export import get_export_service
from core.models.user import User
from schemas.export_schema import ExportRequest, ExportResponse
from services.dataset.export_service import ExportService

router = APIRouter(
    prefix="/export",
    tags=["Export"],
)

@router.post("", response_model=ExportResponse, status_code=status.HTTP_200_OK)
async def export_dataset(
    request: ExportRequest,
    service: ExportService = Depends(get_export_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    return await service.export(user=current_user, request=request)

@router.post("/dataset/{dataset_id}", response_model=ExportResponse)
async def export_entire_dataset(
    dataset_id: UUID,
    format: str,
    service: ExportService = Depends(get_export_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    return await service.export_dataset(user=current_user, dataset_id=dataset_id, format=format)