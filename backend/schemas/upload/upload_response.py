from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class UploadedDocument(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    original_filename: str
    rows_count: int
    columns_count: int
    processing_time_ms: int
    status: str


class UploadResponse(BaseModel):

    document: UploadedDocument
    rows: int
    columns: int
    message: str = "Upload completed successfully."