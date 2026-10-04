from __future__ import annotations
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from core.dependencies.repositories import get_chat_repository, get_chat_message_repository, get_conversation_memory_repository
from backend.repositories.chat_session_repository import ChatRepository
from repositories.ai.chat_message_repository import ChatMessageRepository
from repositories.ai.conversation_memory_repository import ConversationMemoryRepository
from services.chat.chat_session_service import ChatSessionService
from backend.services.chat_message_service import ChatMessageService
from services.ai.conversation_memory_service import ConversationMemoryService

def get_chat_session_service(repository: ChatRepository = Depends(get_chat_repository)) -> ChatSessionService:

    return ChatSessionService(repository=repository)

def get_chat_message_service(repository: ChatMessageRepository = Depends(get_chat_message_repository)) -> ChatMessageService:

    return ChatMessageService(repository=repository)

def get_conversation_memory_service(db: Session = Depends(get_db)) -> ConversationMemoryService:

    return ConversationMemoryService(db)