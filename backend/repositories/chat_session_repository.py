from __future__ import annotations
from uuid import UUID
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, selectinload
from core.constants.conversation import ChatState
from core.models.chat_session import ChatSession
from repositories.base_repository import BaseRepository

class ChatSessionRepository(BaseRepository[ChatSession]):

    def __init__(self, db: Session):
        super().__init__(db, ChatSession)

    def by_dataset(self, dataset_id: UUID) -> list[ChatSession]:
        stmt = select(ChatSession).where(ChatSession.dataset_id == dataset_id).order_by(desc(ChatSession.last_message_at))

        return list(self.db.scalars(stmt).all())

    def latest(self, dataset_id: UUID) -> ChatSession | None:
        stmt = select(ChatSession).where(ChatSession.dataset_id == dataset_id).order_by(desc(ChatSession.last_message_at)).limit(1)

        return self.db.scalar(stmt)

    def active(self, dataset_id: UUID) -> list[ChatSession]:
        stmt = select(ChatSession).where(ChatSession.dataset_id == dataset_id, ChatSession.state == ChatState.ACTIVE,).order_by(desc(ChatSession.last_message_at))

        return list(self.db.scalars(stmt).all())

    def pinned(self, dataset_id: UUID) -> list[ChatSession]:
        stmt = select(ChatSession).where(ChatSession.dataset_id == dataset_id, ChatSession.is_pinned.is_(True),).order_by(desc(ChatSession.last_message_at))

        return list(self.db.scalars(stmt).all())

    def with_messages(self, session_id: UUID) -> ChatSession | None:
        stmt = select(ChatSession).options(selectinload(ChatSession.messages)).where(ChatSession.id == session_id)

        return self.db.scalar(stmt)

    def archive(self, session: ChatSession) -> ChatSession:
        return self.update(session,state=ChatState.ARCHIVED)

    def activate(self, session: ChatSession) -> ChatSession:
        return self.update(session,state=ChatState.ACTIVE)