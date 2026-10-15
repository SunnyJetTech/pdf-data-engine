from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models.processing_job import ProcessingJob, ProcessingJobStatus
from repositories.processing_job_repository import ProcessingJobRepository
from services.base_service import BaseService

class ProcessingJobService(BaseService):

    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.jobs = ProcessingJobRepository(db)

    def get(self, job_id: UUID) -> ProcessingJob:
        job = self.jobs.by_id(job_id)

        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processing job not found.")

        return job

    def get_for_tenant(self, *, job_id: UUID, tenant_id: UUID) -> ProcessingJob:
        job = self.get(job_id)

        if job.tenant_id != tenant_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processing job not found.")

        return job

    def by_tenant(self, *, tenant_id: UUID) -> list[ProcessingJob]:
        return self.jobs.by_tenant(tenant_id)

    def by_dataset(self, *, dataset_id: UUID, tenant_id: UUID) -> list[ProcessingJob]:
        jobs = self.jobs.by_dataset(dataset_id)

        return [job for job in jobs if job.tenant_id == tenant_id]

    def by_document(self, *, document_id: UUID, tenant_id: UUID) -> list[ProcessingJob]:
        jobs = self.jobs.by_document(document_id)

        return [job for job in jobs if job.tenant_id == tenant_id]

    def by_status(self, *, status: ProcessingJobStatus, tenant_id: UUID) -> list[ProcessingJob]:
        jobs = self.jobs.by_status(status)

        return [job for job in jobs if job.tenant_id == tenant_id]

    def set_task_id(self, *, job: ProcessingJob, task_id: str) -> ProcessingJob:
        self.jobs.set_task_id( job=job, task_id=task_id)

        return self.commit_refresh(job)

    def update_progress(self, *, job: ProcessingJob, progress: int, stage: str | None = None, message: str | None = None) -> ProcessingJob:
        self.jobs.update_progress(job=job, progress=progress, stage=stage, message=message)

        return self.commit_refresh(job)

    def mark_queued(self, job: ProcessingJob) -> ProcessingJob:
        self.jobs.mark_queued(job)

        return self.commit_refresh(job)

    def mark_processing(self, job: ProcessingJob) -> ProcessingJob:
        self.jobs.mark_processing(job)

        return self.commit_refresh(job)

    def mark_completed(self, job: ProcessingJob) -> ProcessingJob:
        self.jobs.mark_completed(job)

        return self.commit_refresh(job)

    def mark_failed( self, *, job: ProcessingJob, error_message: str) -> ProcessingJob:
        self.jobs.mark_failed( job=job, error_message=error_message)

        return self.commit_refresh(job)

    def mark_cancelled(self, job: ProcessingJob) -> ProcessingJob:
        self.jobs.mark_cancelled(job)

        return self.commit_refresh(job)