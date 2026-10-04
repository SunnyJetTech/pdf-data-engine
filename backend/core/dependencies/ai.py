from __future__ import annotations
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from core.dependencies.chat import get_chat_session_service, get_chat_message_service, get_conversation_memory_service,
from services.chat.chat_session_service import ChatSessionService
from backend.services.chat_message_service import ChatMessageService
from services.ai.conversation_memory_service import ConversationMemoryService
from services.ai.ai_service import AIService

def get_ai_service(
    db: Session = Depends(get_db),
    chat_sessions: ChatSessionService = Depends(get_chat_session_service),
    chat_messages: ChatMessageService = Depends(get_chat_message_service),
    memory: ConversationMemoryService = Depends(get_conversation_memory_service),
) -> AIService:

    return AIService( db=db, chat_sessions=chat_sessions, chat_messages=chat_messages, memory=memory)