from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel

class ChatRequest(BaseModel):
    dataset_id: UUID
    session_id: UUID | None = None
    message: str