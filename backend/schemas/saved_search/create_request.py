from pydantic import BaseModel, Field
from uuid import UUID

class SavedSearchCreateRequest(BaseModel):

    dataset_id: UUID
    name: str = Field(min_length=1, max_length=255)
    filters: list[dict]