from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.constants.conversation import MessageRole
from core.models.chat_message import ChatMessage
from core.models.chat_session import ChatSession
from repositories.chat_message_repository import ChatMessageRepository
from repositories.chat_session_repository import ChatSessionRepository
from services.base_service import BaseService

class ChatMessageService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

        self.messages = ChatMessageRepository(db)
        self.sessions = ChatSessionRepository(db)

    def get(self, message_id: UUID) -> ChatMessage:
        message = self.messages.by_id(message_id)

        if message is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found.")

        return message

    def history(self, session_id: UUID) -> list[ChatMessage]:

        return self.messages.by_session(session_id)

    def latest(self, session_id: UUID) -> ChatMessage | None:

        return self.messages.latest(session_id)

    def add_user(self, *, actor_id: UUID, session: ChatSession, content: str, metadata: dict | None = None) -> ChatMessage:

        return self._create(actor_id=actor_id, session=session, role=MessageRole.USER, content=content, metadata=metadata)

    def add_assistant(
        self,
        *,
        actor_id: UUID,
        session: ChatSession,
        content: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        provider: str | None = None,
        model: str | None = None,
        finish_reason: str | None = None,
        metadata: dict | None = None,
    ) -> ChatMessage:

        return self._create(
            actor_id=actor_id,
            session=session,
            role=MessageRole.ASSISTANT,
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            provider=provider,
            model=model,
            finish_reason=finish_reason,
            metadata=metadata,
        )

    def add_system(self, *, actor_id: UUID, session: ChatSession, content: str) -> ChatMessage:

        return self._create(actor_id=actor_id, session=session, role=MessageRole.SYSTEM, content=content)

    def delete(self, *, actor_id: UUID, message: ChatMessage) -> None:
        self.messages.delete(message)
        self.commit()

        self.activity.log(
            actor_id=actor_id,
            tenant_id=message.chat_session.dataset.tenant_id,
            action=ActivityAction.MESSAGE_DELETED,
            target_type="chat_message",
            target_id=message.id,
        )

    def _create(
        self,
        *,
        actor_id: UUID,
        session: ChatSession,
        role: MessageRole,
        content: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        provider: str | None = None,
        model: str | None = None,
        finish_reason: str | None = None,
        metadata: dict | None = None,
    ) -> ChatMessage:

        message = ChatMessage(
            chat_session_id=session.id,
            sequence=self.messages.next_sequence(session.id),
            role=role,
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            provider=provider,
            model=model,
            finish_reason=finish_reason,
            metadata=metadata,
        )

        self.messages.add(message)
        self.sessions.update(session, last_message_at=datetime.utcnow(), last_used_at=datetime.utcnow())
        self.commit_refresh(message)

        self.activity.log(
            actor_id=actor_id,
            tenant_id=session.dataset.tenant_id,
            action=ActivityAction.MESSAGE_CREATED,
            target_type="chat_message",
            target_id=message.id,
        )

        return message