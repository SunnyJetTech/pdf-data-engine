from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from core.constants.document_status import DocumentStatus
from core.models.base import BaseModel
from sqlalchemy import Index

if TYPE_CHECKING:
    from .activity import Activity
    from .dataset import Dataset
    from .search import SearchHistory
    from .user import User

class Document(BaseModel):

    __tablename__ = "documents"

    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE",),nullable=False,index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL",),nullable=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255),nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="application/pdf", nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    rows_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    columns_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    has_header: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus), default=DocumentStatus.PROCESSING, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    indexed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    checksum: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    storage_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    mongo_collection: Mapped[str] = mapped_column(String(255), nullable=False)
    
    dataset: Mapped["Dataset"] = relationship(back_populates="documents")
    created_by: Mapped[uuid.UUID | None] = mapped_column( ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by_user: Mapped["User | None"] = relationship( back_populates="documents", cascade="all, delete-orphan")
        
    __table_args__ = (Index("ix_document_dataset_status", "dataset_id", "status"))
    