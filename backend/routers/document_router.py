from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from core.auth import get_current_user_from_cookie
from core.models import User
from schema.response_schema import APIResponse
from schema.document_schema import DocumentResponse, DocumentStatsResponse
from services.document_service import DocumentService
from core.responses_builder import success

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/", response_model=APIResponse)
def get_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    documents = DocumentService.get_user_documents(db=db, user_id=current_user.id)

    return success(
        data=[DocumentService.serialize(doc) for doc in documents],
        message="Documents retrieved successfully.",
    )


@router.get("/{document_id}", response_model=APIResponse)
def get_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    document = DocumentService.get_document(db=db, user_id=current_user.id, document_id=document_id)

    return success(
        data=DocumentService.serialize(document),
        message="Document retrieved successfully.",
    )


@router.get("/{document_id}/columns", response_model=APIResponse)
def get_columns(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    columns = DocumentService.get_columns(db=db, user_id=current_user.id, document_id=document_id)

    return success(
        data=columns,
        message="Columns retrieved successfully.",
    )

@router.get("/{document_id}/sample", response_model=APIResponse)
def get_sample(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    sample = DocumentService.get_sample(db=db, user_id=current_user.id, document_id=document_id)

    return success(
        data=sample,
        message="Sample retrieved successfully.",
    )

@router.get("/{document_id}/stats", response_model=APIResponse)
def get_statistics(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    stats = DocumentService.get_statistics(db=db, user_id=current_user.id, document_id=document_id)

    return success(
        data=stats,
        message="Statistics retrieved successfully.",
    )

@router.delete("/{document_id}", response_model=APIResponse)
def delete_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    DocumentService.delete(db=db, user_id=current_user.id, document_id=document_id)

    return success(
        message="Document deleted successfully.",
    )