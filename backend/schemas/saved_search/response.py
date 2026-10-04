from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class SavedSearchResponse(BaseModel):

    id: UUID
    dataset_id: UUID
    name: str
    filters: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True