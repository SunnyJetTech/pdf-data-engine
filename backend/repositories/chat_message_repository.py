from __future__ import annotations
from uuid import UUID
from sqlalchemy import delete, desc, func, select
from sqlalchemy.orm import Session
from core.models.chat_message import ChatMessage
from repositories.base_repository import BaseRepository

class ChatMessageRepository(BaseRepository[ChatMessage]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=ChatMessage)

    def by_id(self, message_id: UUID) -> ChatMessage | None:
        stmt = select(ChatMessage).where(ChatMessage.id == message_id)

        return self.db.scalar(stmt)

    def by_session(self, session_id: UUID) -> list[ChatMessage]:
        stmt = select(ChatMessage).where(ChatMessage.chat_session_id == session_id).order_by(ChatMessage.sequence)

        return list(self.db.scalars(stmt).all())

    def latest(self, session_id: UUID) -> ChatMessage | None:
        stmt = select(ChatMessage).where(ChatMessage.chat_session_id == session_id).order_by(desc(ChatMessage.sequence)).limit(1)

        return self.db.scalar(stmt)

    def next_sequence(self, session_id: UUID) -> int:
        stmt = select(func.max(ChatMessage.sequence)).where(ChatMessage.chat_session_id == session_id)
        current = self.db.scalar(stmt)

        return (current or 0) + 1

    def delete_by_session(self, session_id: UUID) -> None:
        stmt = delete(ChatMessage).where(ChatMessage.chat_session_id == session_id)

        self.db.execute(stmt)