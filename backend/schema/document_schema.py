from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    filename: str
    mongo_collection: str
    rows: int
    columns: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class DocumentStatsResponse(BaseModel):
    rows: int
    columns: int
    uploaded: datetime

class SearchResultResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[dict[str, Any]]

class SearchHistoryResponse(BaseModel):
    id: int
    document_id: int
    column_name: str
    operator: str
    search_value: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }