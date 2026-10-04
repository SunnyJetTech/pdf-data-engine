from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from core.constants.document_status import DocumentStatus

class DocumentResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    created_by: UUID | None
    filename: str
    original_filename: str
    mime_type: str
    file_size: int
    rows_count: int
    columns_count: int
    has_header: bool
    processing_time_ms: int
    status: DocumentStatus
    error_message: str | None
    indexed: bool
    checksum: str | None
    storage_path: str | None
    mongo_collection: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class DocumentListResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    filename: str
    original_filename: str
    mime_type: str
    file_size: int
    rows_count: int
    columns_count: int
    status: DocumentStatus
    indexed: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class DocumentStatsResponse(BaseModel):
    documents_count: int
    rows_count: int
    columns_count: int
    indexed_count: int
    processing_count: int
    failed_count: int

class DocumentUploadResponse(BaseModel):
    document: DocumentResponse
    rows: int
    columns: int

    model_config = ConfigDict(
        from_attributes=True,
    )
