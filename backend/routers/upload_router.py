from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from core.auth import get_current_user_from_cookie
from core.dependencies.upload import get_upload_service
from core.models.user import User
from schemas.upload.upload_response import UploadResponse
from services.upload.upload_service import UploadService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

@router.post("/pdf", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    dataset_id: UUID = Form(...),
    has_header: bool = Form(True),
    file: UploadFile = File(...),
    service: UploadService = Depends(get_upload_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A filename is required.")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported.")

    try:
        return await service.upload_pdf(
            dataset_id=dataset_id,
            created_by=current_user.id,
            pdf_source=file.file,
            original_filename=file.filename,
            has_header=has_header,
        )

    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
