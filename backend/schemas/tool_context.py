from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import pandas as pd
from sqlalchemy.orm import Session

from core.models import User, Dataset
from core.models.chat_session import ChatSession


@dataclass(slots=True)
class ToolContext:
    
    db: Session
    user: User
    dataset: Dataset
    dataframe: pd.DataFrame
    session: ChatSession
    memory: dict[str, dict[str, Any]]
    client_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    cache: dict[str, Any] = field(default_factory=dict)