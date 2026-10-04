from __future__ import annotations
from typing import Any
from uuid import UUID
from sqlalchemy.orm import Session
from core.models.chat_message import ChatMessage
from services.ai.conversation_memory_service import ConversationMemoryService
from services.ai.prompt_builder_service import PromptBuilderService
from services.ai.system_prompt_service import SystemPromptService
from services.chat_message_service import ChatMessageService

class PromptService:
    def __init__(self, db: Session) ->None:

        self.memory_service = ConversationMemoryService(db)
        self.chat_service = ChatMessageService(db)

    def build( self, *, chat_session_id: UUID, retrieved_context: list[str], user_message: str) -> list[dict[str, str]]:

        return PromptBuilderService.build(
            system_prompt=self.system_prompt(),
            history=self.history(chat_session_id=chat_session_id),
            memory=self.memory(chat_session_id=chat_session_id),
            retrieved_context=retrieved_context,
            user_message=user_message,
        )

    def history(self, *, chat_session_id: UUID) -> list[ChatMessage]:

        return self.chat_service.history(chat_session_id)

    def memory(self, *, chat_session_id: UUID) -> dict[str, dict[str, Any]]:

        return self.memory_service.recall_all(chat_session_id=chat_session_id)

    @staticmethod
    def system_prompt() -> str:

        return SystemPromptService.build()