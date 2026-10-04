from __future__ import annotations
import uuid
from typing import Any
from sqlalchemy import Enum, ForeignKey, Float, Index, JSON, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.constants.conversation import ToolExecutionStatus
from core.models.base import BaseModel
from core.models.chat_message import ChatMessage
from datetime import datetime

class ToolExecution(BaseModel):
    __tablename__ = "tool_executions"

    chat_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[ToolExecutionStatus] = mapped_column(Enum(ToolExecutionStatus), default=ToolExecutionStatus.PENDING, nullable=False)
    arguments: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    execution_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    error: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    provider_call_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    chat_message: Mapped["ChatMessage"] = relationship( "ChatMessage", back_populates="tool_executions")

    __table_args__ = (
        Index("ix_tool_execution_message", "chat_message_id"),
        Index("ix_tool_execution_tool", "tool_name"),
        Index("ix_tool_execution_status", "status"),
        UniqueConstraint("chat_message_id", "sequence", name="uq_tool_execution_sequence"),
    )