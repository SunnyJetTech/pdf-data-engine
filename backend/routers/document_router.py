from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from core.auth import get_current_user_from_cookie
from core.dependencies.dataset import get_dataset_service
from core.dependencies.document import get_document_service
from core.models.user import User
from schemas.document_schema import DocumentResponse
from services.dataset_service import DatasetService
from services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

def _ensure_dataset_access(*, dataset_service: DatasetService, current_user: User, dataset_id: UUID):
    dataset = dataset_service.get(dataset_id)

    if dataset.tenant_id != current_user.tenant_id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Dataset does not belong to your workspace.")

    return dataset

def _get_document_for_user(*, document_service: DocumentService, current_user: User, document_id: UUID):
    document = document_service.get(document_id)

    if document.dataset.tenant_id != current_user.tenant_id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    return document

@router.get("/dataset/{dataset_id}", response_model=list[DocumentResponse])
def list_documents(
    dataset_id: UUID,
    dataset_service: DatasetService = Depends(get_dataset_service),
    document_service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    dataset = _ensure_dataset_access(dataset_service=dataset_service, current_user=current_user, dataset_id=dataset_id)

    return document_service.by_dataset(dataset.id)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: UUID,
    document_service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    return _get_document_for_user(document_service=document_service, current_user=current_user, document_id=document_id)

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: UUID,
    document_service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_user_from_cookie),
):
    document = _get_document_for_user(document_service=document_service, current_user=current_user, document_id=document_id)

    document_service.delete(document=document, actor_id=current_user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
