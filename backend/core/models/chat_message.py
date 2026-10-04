from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey, Index, Integer, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.constants.conversation import MessageRole
from core.models.base import BaseModel

if TYPE_CHECKING:
    from .chat_session import ChatSession
    from .tool_execution import ToolExecution

class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"

    chat_session_id: Mapped[uuid.UUID] = mapped_column( ForeignKey(     "chat_sessions.id",     ondelete="CASCADE", ), nullable=False)
    sequence: Mapped[int] = mapped_column( Integer, nullable=False)
    role: Mapped[MessageRole] = mapped_column( Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column( Text, nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    finish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_message_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chat_messages.id", ondelete="SET NULL"), nullable=True)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    parent: Mapped["ChatMessage"] = relationship(remote_side="ChatMessage.id")
    chat_session: Mapped["ChatSession"] = relationship( "ChatSession", back_populates="messages")
    tool_executions: Mapped[list["ToolExecution"]] = relationship( "ToolExecution", back_populates="chat_message", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("chat_session_id", "sequence", name="uq_chat_message_sequence"),
        Index("ix_chat_message_session", "chat_session_id"),
        Index( "ix_chat_message_sequence", "chat_session_id", "sequence"),
    )