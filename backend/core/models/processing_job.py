from __future__ import annotations
import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.dataset import Dataset
    from core.models.document import Document
    from core.models.tenant import Tenant

class ProcessingJobStatus(str, enum.Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled" 
    
class ProcessingJobType(str, enum.Enum):
    DATASET_IMPORT = "dataset_import"
    DOCUMENT_INGESTION = "document_ingestion"
    DATA_TRANSFORMATION = "data_transformation"
    AI_ENRICHMENT = "ai_enrichment"
    EMBEDDING_GENERATION = "embedding_generation"
    EXPORT = "export"

class ProcessingJob(BaseModel):
    __tablename__ = "processing_jobs"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"),nullable=False)
    dataset_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("datasets.id", ondelete="SET NULL"),nullable=True)
    document_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("documents.id", ondelete="SET NULL"),nullable=True)
    task_id: Mapped[str | None] = mapped_column(String(255),nullable=True,index=True)
    job_type: Mapped[ProcessingJobType] = mapped_column(Enum(ProcessingJobType, name="processing_job_type"), nullable=False, index=True)
    status: Mapped[ProcessingJobStatus] = mapped_column(
        Enum(ProcessingJobStatus, name="processing_job_status"),
        nullable=False,
        default=ProcessingJobStatus.PENDING,
        index=True,
    )
    stage: Mapped[str | None] = mapped_column(String(100), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    tenant: Mapped["Tenant"] = relationship()
    dataset: Mapped["Dataset | None"] = relationship()
    document: Mapped["Document | None"] = relationship()

    __table_args__ = (
        Index("ix_processing_job_tenant_status", "tenant_id", "status"),
        Index("ix_processing_job_tenant_created", "tenant_id", "created_at"),
    )