from __future__ import annotations
from typing import Any
from uuid import UUID
from pydantic import BaseModel


class ChatResponse(BaseModel):

    session_id: UUID
    provider: str
    model: str
    message: str
    tool_calls: list[dict[str, Any]]
    usage: dict[str, int]