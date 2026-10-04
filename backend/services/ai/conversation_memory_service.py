from __future__ import annotations
from typing import Any
from uuid import UUID
from sqlalchemy.orm import Session
from repositories.ai.conversation_memory_repository import ConversationMemoryRepository

class ConversationMemoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.memories = ConversationMemoryRepository(db)

    def remember(self, *, chat_session_id: UUID, namespace: str, key: str, value: Any) -> None:
        self.memories.set(chat_session_id=chat_session_id, namespace=namespace, key=key, value=value)

        self.db.commit()

    def recall(self, *, chat_session_id: UUID, namespace: str) -> dict[str, Any]:
        memories = self.memories.get_namespace(chat_session_id, namespace)

        return {memory.key: memory.value for memory in memories}

    def recall_all(self, *, chat_session_id: UUID) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}

        for memory in self.memories.all_memory(chat_session_id):
            result.setdefault(memory.namespace, {})
            result[memory.namespace][memory.key] = memory.value

        return result

    def recall_key(self, *, chat_session_id: UUID, namespace: str, key: str) -> Any | None:
        memory = self.memories.get(chat_session_id=chat_session_id, namespace=namespace, key=key)

        return None if memory is None else memory.value

    def exists(self, *, chat_session_id: UUID, namespace: str, key: str) -> bool:

        return (self.recall_key(chat_session_id=chat_session_id, namespace=namespace, key=key) is not None)

    def forget(self, *, chat_session_id: UUID, namespace: str, key: str) -> None:
        self.memories.forget(chat_session_id=chat_session_id, namespace=namespace, key=key)

        self.db.commit()

    def clear(self, *, chat_session_id: UUID) -> None:
        self.memories.clear(chat_session_id)
        self.db.commit()