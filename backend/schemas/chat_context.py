from dataclasses import dataclass
from sqlalchemy.orm import Session
from core.models import User
from core.models.chat_session import ChatSession
from typing import Any

@dataclass(slots=True)
class ChatContext:

    db: Session
    user: User
    session: ChatSession
    client_id: str | None = None
    metadata: dict[str, Any] | None = None