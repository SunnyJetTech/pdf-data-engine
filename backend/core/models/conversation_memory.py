from __future__ import annotations
import uuid
from sqlalchemy import ForeignKey, Index, JSON, String, UniqueConstraint, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel
from core.models.chat_session import ChatSession
from datetime import datetime

class ConversationMemory(BaseModel):
    __tablename__ = "conversation_memory"

    chat_session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    namespace: Mapped[str] = mapped_column(String(100), nullable=False)
    key: Mapped[str] = mapped_column(String(150), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    memory_type: Mapped[str] = mapped_column(String(50), default="fact", nullable=False)
    importance: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    last_accessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="conversation_memory")

    __table_args__ = (
            UniqueConstraint("chat_session_id", "namespace", "key", name="uq_conversation_memory",),
            Index("ix_conversation_memory_session", "chat_session_id",),Index("ix_conversation_memory_namespace", "namespace",),
            Index("ix_conversation_memory_type", "memory_type"),
        )