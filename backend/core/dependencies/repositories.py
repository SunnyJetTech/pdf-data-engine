from __future__ import annotations
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from repositories.dataset_repository import DatasetRepository
from repositories.document_repository import DocumentRepository
from backend.repositories.chat_session_repository import ChatRepository
from repositories.ai.chat_message_repository import ChatMessageRepository
from repositories.ai.conversation_memory_repository import ConversationMemoryRepository
from repositories.search_history_repository import SearchHistoryRepository
from repositories.saved_search_repository import SavedSearchRepository
from repositories.mongo_repository import MongoRepository

def get_dataset_repository(db: Session = Depends(get_db)) -> DatasetRepository:

    return DatasetRepository(db)

def get_document_repository(db: Session = Depends(get_db)) -> DocumentRepository:

    return DocumentRepository(db)

def get_chat_repository(db: Session = Depends(get_db)) -> ChatRepository:

    return ChatRepository(db)

def get_chat_message_repository(db: Session = Depends(get_db)) -> ChatMessageRepository:

    return ChatMessageRepository(db)

def get_conversation_memory_repository(db: Session = Depends(get_db)) -> ConversationMemoryRepository:

    return ConversationMemoryRepository(db)

def get_search_history_repository(db: Session = Depends(get_db)) -> SearchHistoryRepository:

    return SearchHistoryRepository(db)

def get_saved_search_repository(db: Session = Depends(get_db)) -> SavedSearchRepository:

    return SavedSearchRepository(db)

def get_mongo_repository() -> MongoRepository:

    return MongoRepository()