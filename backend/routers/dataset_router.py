from __future__ import annotations

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from core.auth import get_current_user_from_cookie
from core.dependencies.dataset import get_dataset_service

from core.models.user import User

from schemas.dataset_schema import DatasetCreateRequest
from schemas.dataset_schema import DatasetUpdateRequest
from schemas.dataset_schema import DatasetResponse

from backend.services.dataset_service import DatasetService


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


# ---------------------------------------------------------------------
# List datasets
# ---------------------------------------------------------------------

@router.get(
    "",
    response_model=list[DatasetResponse],
)
async def list_datasets(

    service: DatasetService = Depends(
        get_dataset_service,
    ),

    current_user: User = Depends(
        get_current_user_from_cookie,
    ),

):

    return await service.list(
        user=current_user,
    )


# ---------------------------------------------------------------------
# Get dataset
# ---------------------------------------------------------------------

@router.get(
    "/{dataset_id}",
    response_model=DatasetResponse,
)
async def get_dataset(

    dataset_id: UUID,

    service: DatasetService = Depends(
        get_dataset_service,
    ),

    current_user: User = Depends(
        get_current_user_from_cookie,
    ),

):

    dataset = await service.get(
        dataset_id=dataset_id,
        user=current_user,
    )

    if dataset is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found.",
        )

    return dataset


# ---------------------------------------------------------------------
# Create dataset
# ---------------------------------------------------------------------

@router.post(
    "",
    response_model=DatasetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dataset(

    request: DatasetCreateRequest,

    service: DatasetService = Depends(
        get_dataset_service,
    ),

    current_user: User = Depends(
        get_current_user_from_cookie,
    ),

):

    return await service.create(
        user=current_user,
        request=request,
    )


# ---------------------------------------------------------------------
# Update dataset
# ---------------------------------------------------------------------

@router.patch(
    "/{dataset_id}",
    response_model=DatasetResponse,
)
async def update_dataset(

    dataset_id: UUID,

    request: DatasetUpdateRequest,

    service: DatasetService = Depends(
        get_dataset_service,
    ),

    current_user: User = Depends(
        get_current_user_from_cookie,
    ),

):

    return await service.update(
        dataset_id=dataset_id,
        user=current_user,
        request=request,
    )


# ---------------------------------------------------------------------
# Delete dataset
# ---------------------------------------------------------------------

@router.delete(
    "/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_dataset(

    dataset_id: UUID,

    service: DatasetService = Depends(
        get_dataset_service,
    ),

    current_user: User = Depends(
        get_current_user_from_cookie,
    ),

):

    await service.delete(
        dataset_id=dataset_id,
        user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )