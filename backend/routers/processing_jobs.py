from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.processing_job import ProcessingJobStatus
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.processing_job_service import ProcessingJobService

router = APIRouter(
    prefix="/processing-jobs",
    tags=["Processing Jobs"],
)

@router.get("", response_model=APIResponse)
def list_processing_jobs(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = ProcessingJobService(db)
    jobs = service.by_tenant(tenant_id=current_user.current_tenant_id)

    return success(jobs, "Processing jobs retrieved successfully.")

@router.get("/dataset/{dataset_id}", response_model=APIResponse)
def list_dataset_processing_jobs(dataset_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = ProcessingJobService(db)

    jobs = service.by_dataset(dataset_id=dataset_id, tenant_id=current_user.current_tenant_id)

    return success(jobs, "Dataset processing jobs retrieved successfully.")

@router.get("/document/{document_id}", response_model=APIResponse)
def list_document_processing_jobs(document_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = ProcessingJobService(db)
    jobs = service.by_document(document_id=document_id, tenant_id=current_user.current_tenant_id)

    return success(jobs, "Document processing jobs retrieved successfully.")

@router.get("/status/{job_status}", response_model=APIResponse)
def list_processing_jobs_by_status(job_status: ProcessingJobStatus, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = ProcessingJobService(db)
    jobs = service.by_status(status=job_status, tenant_id=current_user.current_tenant_id)

    return success(jobs, "Processing jobs retrieved successfully.")

@router.get("/{job_id}", response_model=APIResponse)
def get_processing_job(job_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = ProcessingJobService(db)

    job = service.get_for_tenant(job_id=job_id, tenant_id=current_user.current_tenant_id)

    return success(job, "Processing job retrieved successfully.")