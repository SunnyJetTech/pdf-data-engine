from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import pandas as pd
from sqlalchemy.orm import Session
from core.models.chat_session import ChatSession
from core.models.dataset import Dataset
from core.models.user import User
from services.ai.conversation_memory_service import ConversationMemoryService

@dataclass(slots=True)
class ToolContext:
    db: Session
    user: User
    dataset: Dataset
    session: ChatSession | None = None
    dataframe: pd.DataFrame | None = None
    memory: ConversationMemoryService | None = None

    runtime: dict[str, Any] = field(default_factory=dict)