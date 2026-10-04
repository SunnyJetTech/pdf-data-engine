from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    dataset_id: UUID
    query: str = Field(..., min_length=1, max_length=5000)
    limit: int = Field(default=20, ge=1, le=100)
