from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field

class SearchResponse(BaseModel):
    query: str
    count: int = Field(ge=0)
    results: list[dict[str, Any]]
