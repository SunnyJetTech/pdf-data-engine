from __future__ import annotations
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.document import Document
from core.models.user import User
from core.pagination import Pagination
from core.responses_builder import success
from db.database import get_db
from schemas.document_schema import DocumentListResponse, DocumentResponse
from schemas.response_schema import APIResponse
from services.document_service import DocumentService
from services.dataset_service import DatasetService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

def _document_service(db: Session) -> DocumentService:
    return DocumentService(db)


def _dataset_service(db: Session) -> DatasetService:
    return DatasetService(db)

def _get_document(document_id: UUID, current_user: User, service: DocumentService) -> Document:
    return service.get_for_tenant(document_id=document_id, tenant_id=current_user.current_tenant_id)

@router.get("/dataset/{dataset_id}", response_model=APIResponse)
def list_documents(
    dataset_id: UUID,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    datasets = _dataset_service(db)
    dataset = datasets.get(dataset_id)

    if dataset.tenant_id != current_user.current_tenant_id:
        return success([], "Documents retrieved successfully.")

    pagination = Pagination(page=page, page_size=page_size)
    documents = _document_service(db).paginate_by_dataset(dataset_id=dataset.id, pagination=pagination)

    return success(documents, "Documents retrieved successfully.")


@router.get("/{document_id}", response_model=APIResponse)
def get_document(document_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = _document_service(db)
    document = _get_document(document_id=document_id, current_user=current_user, service=service)

    return success(document, "Document retrieved successfully.")


@router.get("/{document_id}/status", response_model=APIResponse)
def get_document_status(document_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = _document_service(db)

    document = _get_document(document_id=document_id, current_user=current_user, service=service)

    return success(
        {
            "id": document.id,
            "status": document.status,
            "indexed": document.indexed,
            "error_message": document.error_message,
        },
        "Document status retrieved successfully.",
    )


@router.post( "/{document_id}/processing", response_model=APIResponse)
def mark_document_processing( document_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = _document_service(db)

    document = _get_document(document_id=document_id, current_user=current_user, service=service)
    document = service.mark_processing(document)

    return success( document, "Document marked as processing.")


@router.post("/{document_id}/ready", response_model=APIResponse)
def mark_document_ready(
    document_id: UUID,
    rows: Annotated[int, Query(ge=0)],
    columns: Annotated[int, Query(ge=0)],
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    service = _document_service(db)
    document = _get_document(document_id=document_id, current_user=current_user, service=service)
    document = service.mark_ready( document=document, rows=rows, columns=columns)

    return success( document, "Document marked as ready.")


@router.post("/{document_id}/failed", response_model=APIResponse)
def mark_document_failed(
    document_id: UUID,
    error: Annotated[str, Query(min_length=1)],
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    service = _document_service(db)
    document = _get_document(document_id=document_id, current_user=current_user, service=service)
    document = service.mark_failed( document=document, error=error)

    return success(document, "Document marked as failed.")

@router.delete( "/{document_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def delete_document( document_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = _document_service(db)
    document = _get_document(document_id=document_id, current_user=current_user, service=service)
    service.delete(document=document, actor_id=current_user.id)

    return success(None, "Document deleted successfully.",)