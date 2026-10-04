from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.models.chat_session import ChatSession
from core.models.dataset import Dataset
from repositories.chat_session_repository import ChatSessionRepository
from services.base_service import BaseService

class ChatService(BaseService):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

        self.sessions = ChatSessionRepository(db)

    def get(self, session_id: UUID) -> ChatSession:
        session = self.sessions.get(session_id)

        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found.")

        return session

    def by_dataset(self, dataset_id: UUID) -> list[ChatSession]:

        return self.sessions.by_dataset(dataset_id)

    def latest(self, dataset_id: UUID) -> ChatSession | None:

        return self.sessions.latest(dataset_id)

    def active(self, dataset_id: UUID) -> list[ChatSession]:

        return self.sessions.active(dataset_id)

    def pinned(self, dataset_id: UUID) -> list[ChatSession]:

        return self.sessions.pinned(dataset_id)

    def with_messages(self, session_id: UUID) -> ChatSession | None:

        return self.sessions.with_messages(session_id)

    def create( self, *, actor_id: UUID, dataset: Dataset, title: str | None = None) -> ChatSession:
        session = ChatSession( dataset_id=dataset.id, created_by=actor_id, title=title, title_generated=False)

        self.sessions.add(session)
        self.commit_refresh(session)
        self._log_created(actor_id, session)

        return session

    def rename(self, *, session: ChatSession, title: str) -> ChatSession:
        self.sessions.update(session, title=title)

        return self.commit_refresh(session)

    def pin(self, session: ChatSession) -> ChatSession:
        self.sessions.update(session, is_pinned=True)

        return self.commit_refresh(session)

    def unpin(self, session: ChatSession) -> ChatSession:
        self.sessions.update(session, is_pinned=False)

        return self.commit_refresh(session)

    def archive(self, session: ChatSession) -> ChatSession:
        self.sessions.archive(session)

        return self.commit_refresh(session)

    def activate(self, session: ChatSession) -> ChatSession:
        self.sessions.activate(session)

        return self.commit_refresh(session)

    def delete(self, *, actor_id: UUID, session: ChatSession) -> None:
        self.sessions.delete(session)
        self.commit()
        self._log_deleted( actor_id, session)

    def _log_created(self, actor_id: UUID, session: ChatSession) -> None:
        self.activity.log(
            actor_id=actor_id,
            tenant_id=session.dataset.tenant_id,
            action=ActivityAction.CHAT_CREATED,
            target_type="chat_session",
            target_id=session.id,
        )

    def _log_deleted(self, actor_id: UUID, session: ChatSession) -> None:

        self.activity.log(
            actor_id=actor_id,
            tenant_id=session.dataset.tenant_id,
            action=ActivityAction.CHAT_DELETED,
            target_type="chat_session",
            target_id=session.id,
        )