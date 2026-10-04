from __future__ import annotations
from typing import Any
from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from core.models.conversation_memory import ConversationMemory
from repositories.base_repository import BaseRepository

class ConversationMemoryRepository(BaseRepository[ConversationMemory]):

    def __init__(self, db: Session):
        super().__init__(db, ConversationMemory)

    def get(self, chat_session_id: UUID, namespace: str, key: str) -> ConversationMemory | None:

        stmt = select(ConversationMemory).where(ConversationMemory.chat_session_id == chat_session_id, ConversationMemory.namespace == namespace, ConversationMemory.key == key)

        return self.db.scalar(stmt)

    def get_namespace(self, chat_session_id: UUID, namespace: str) -> list[ConversationMemory]:

        stmt = select(ConversationMemory).where(ConversationMemory.chat_session_id == chat_session_id, ConversationMemory.namespace == namespace)

        return list(self.db.scalars(stmt).all())

    def all_memory(self, chat_session_id: UUID) -> list[ConversationMemory]:

        stmt = select(ConversationMemory).where(ConversationMemory.chat_session_id == chat_session_id,)

        return list(self.db.scalars(stmt).all())

    def set(self, *, chat_session_id: UUID, namespace: str, key: str, value: Any) -> ConversationMemory:

        memory = self.get(chat_session_id, namespace, key)

        if memory:
            return self.update(memory, value=value)

        return self.create(chat_session_id=chat_session_id, namespace=namespace, key=key, value=value)

    def forget(self, *, chat_session_id: UUID, namespace: str, key: str) -> None:

        memory = self.get(chat_session_id, namespace, key)

        if memory:
            self.delete(memory)

    def clear(self, chat_session_id: UUID) -> None:

        stmt = delete(ConversationMemory).where(ConversationMemory.chat_session_id == chat_session_id,)

        self.db.execute(stmt)