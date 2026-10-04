from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.models.processing_job import ProcessingJob, ProcessingJobStatus
from repositories.base_repository import BaseRepository

class ProcessingJobRepository(BaseRepository[ProcessingJob]):

    def __init__(self, db: Session) -> None:
        super().__init__(db=db, model=ProcessingJob)

    def by_id(self, job_id: UUID) -> ProcessingJob | None:
        stmt = select(ProcessingJob).where(ProcessingJob.id == job_id)

        return self.db.scalar(stmt)

    def by_task_id(self, task_id: str) -> ProcessingJob | None:
        stmt = select(ProcessingJob).where(ProcessingJob.task_id == task_id)

        return self.db.scalar(stmt)

    def by_tenant(self, tenant_id: UUID) -> list[ProcessingJob]:
        stmt = (
            select(ProcessingJob)
            .where(ProcessingJob.tenant_id == tenant_id)
            .order_by(ProcessingJob.created_at.desc(), ProcessingJob.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def by_dataset(self, dataset_id: UUID) -> list[ProcessingJob]:
        stmt = (
            select(ProcessingJob)
            .where(ProcessingJob.dataset_id == dataset_id)
            .order_by(ProcessingJob.created_at.desc(), ProcessingJob.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def by_document(self, document_id: UUID) -> list[ProcessingJob]:
        stmt = (
            select(ProcessingJob)
            .where(ProcessingJob.document_id == document_id)
            .order_by(ProcessingJob.created_at.desc(), ProcessingJob.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    def by_status(self, status: ProcessingJobStatus) -> list[ProcessingJob]:
        stmt = (
            select(ProcessingJob)
            .where(ProcessingJob.status == status)
            .order_by( ProcessingJob.created_at.asc(), ProcessingJob.id.asc())
        )

        return list(self.db.scalars(stmt).all())

    def set_task_id(self, *, job: ProcessingJob, task_id: str) -> ProcessingJob:
        job.task_id = task_id
        return job

    def update_progress(self, *, job: ProcessingJob, progress: int, stage: str | None = None, message: str | None = None) -> ProcessingJob:
        job.progress = max(0, min(progress, 100))

        if stage is not None:
            job.stage = stage

        if message is not None:
            job.message = message

        return job

    def mark_queued(self, job: ProcessingJob) -> ProcessingJob:
        job.status = ProcessingJobStatus.QUEUED
        
        return job

    def mark_processing(self, job: ProcessingJob) -> ProcessingJob:
        job.status = ProcessingJobStatus.PROCESSING
        
        return job

    def mark_completed(self, job: ProcessingJob) -> ProcessingJob:
        job.status = ProcessingJobStatus.COMPLETED
        job.progress = 100
        
        return job

    def mark_failed(self, *, job: ProcessingJob, error_message: str) -> ProcessingJob:
        job.status = ProcessingJobStatus.FAILED
        job.error_message = error_message
        
        return job

    def mark_cancelled(self, job: ProcessingJob) -> ProcessingJob:
        job.status = ProcessingJobStatus.CANCELLED
        
        return job