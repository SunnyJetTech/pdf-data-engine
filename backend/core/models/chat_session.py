from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.constants.conversation import ChatState
from core.models.base import BaseModel
from core.models.dataset import Dataset
from core.models.chat_message import ChatMessage
from core.models.conversation_memory import ConversationMemory
from core.models.user import User

class ChatSession(BaseModel):
    __tablename__ = "chat_sessions"

    dataset_id: Mapped[uuid.UUID] = mapped_column( ForeignKey(     "datasets.id",     ondelete="CASCADE", ), nullable=False)
    title: Mapped[str | None] = mapped_column( String(255), nullable=True)
    title_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    state: Mapped[ChatState] = mapped_column( Enum(ChatState), default=ChatState.ACTIVE, nullable=False)
    is_pinned: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False)
    last_message_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    dataset: Mapped["Dataset"] = relationship( "Dataset", back_populates="chat_sessions")
    messages: Mapped[list["ChatMessage"]] = relationship( "ChatMessage", back_populates="chat_session", cascade="all, delete-orphan", order_by="ChatMessage.sequence")
    conversation_memory: Mapped[list["ConversationMemory"]] = relationship( "ConversationMemory", back_populates="chat_session", cascade="all, delete-orphan")
    created_by_user: Mapped["User"] = relationship(back_populates="chat_sessions")
    
    __table_args__ = Index( "ix_chat_dataset_state", "dataset_id", "state"), Index( "ix_chat_last_message", "last_message_at")