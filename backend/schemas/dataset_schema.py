from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from core.pagination import Page

class DatasetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None

class DatasetCreate(DatasetBase):
    pass

class DatasetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None

class DatasetArchive(BaseModel):
    archived: bool = True

class DatasetResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    created_by: UUID | None
    name: str
    slug: str
    description: str | None
    storage_identifier: str
    status: str
    documents_count: int
    rows_count: int
    columns_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class DatasetStatistics(BaseModel):
    documents: int
    rows: int
    columns: int

class DatasetDetail(DatasetResponse):
    statistics: DatasetStatistics

class DatasetPage(Page[DatasetResponse]):
    pass