from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.dataset_schema import DatasetDetail, DatasetPage, DatasetResponse, DatasetStatistics, DatasetUpdate
from schemas.response_schema import APIResponse
from services.dataset_service import DatasetService

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)

def _current_tenant_id(current_user: User) -> UUID:
    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a current tenant.")

    return tenant_id

def _owned_dataset(*, service: DatasetService, dataset_id: UUID, tenant_id: UUID):
    dataset = service.get(dataset_id)

    if dataset.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this dataset.")

    return dataset

@router.get("", response_model=APIResponse)
def list_datasets( current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)
    datasets = service.by_tenant(tenant_id)

    return success(
        [DatasetResponse.model_validate(dataset) for dataset in datasets],
        "Datasets retrieved successfully.",
    )

@router.get("/{dataset_id}", response_model=APIResponse)
def get_dataset(dataset_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)

    dataset = _owned_dataset(service=service, dataset_id=dataset_id, tenant_id=tenant_id)

    return success(DatasetResponse.model_validate(dataset), "Dataset retrieved successfully.")

@router.get("/slug/{slug}", response_model=APIResponse)
def get_dataset_by_slug(slug: str, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)

    dataset = service.by_slug(tenant_id=tenant_id, slug=slug)

    return success(DatasetResponse.model_validate(dataset), "Dataset retrieved successfully.")

@router.get("/{dataset_id}/statistics", response_model=APIResponse)
def get_dataset_statistics(dataset_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)
    dataset = _owned_dataset(service=service, dataset_id=dataset_id, tenant_id=tenant_id)

    statistics = DatasetStatistics(documents=dataset.documents_count, rows=dataset.rows_count, columns=dataset.columns_count)

    return success( statistics, "Dataset statistics retrieved successfully.")

@router.patch("/{dataset_id}", response_model=APIResponse)
def update_dataset(dataset_id: UUID, payload: DatasetUpdate, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)
    dataset = _owned_dataset( service=service, dataset_id=dataset_id, tenant_id=tenant_id)

    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        return success(DatasetResponse.model_validate(dataset), "No dataset changes were provided.")

    dataset = service.update(dataset=dataset, **changes)

    return success(DatasetResponse.model_validate(dataset), "Dataset updated successfully.")

@router.post("/{dataset_id}/archive", response_model=APIResponse)
def archive_dataset(dataset_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)

    dataset = _owned_dataset(service=service, dataset_id=dataset_id, tenant_id=tenant_id)
    dataset = service.archive(dataset=dataset, actor_id=current_user.id)

    return success(DatasetResponse.model_validate(dataset), "Dataset archived successfully.")

@router.post("/{dataset_id}/restore", response_model=APIResponse)
def restore_dataset(dataset_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = DatasetService(db)

    dataset = _owned_dataset(service=service, dataset_id=dataset_id, tenant_id=tenant_id)
    dataset = service.restore(dataset=dataset, actor_id=current_user.id)

    return success(DatasetResponse.model_validate(dataset), "Dataset restored successfully.")


@router.delete("/{dataset_id}", response_model=APIResponse)
def delete_dataset( dataset_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = DatasetService(db)
    dataset = _owned_dataset( service=service, dataset_id=dataset_id, tenant_id=tenant_id)
    service.delete(dataset=dataset, actor_id=current_user.id)

    return success(message="Dataset deleted successfully.")