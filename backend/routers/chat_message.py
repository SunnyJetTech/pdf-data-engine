from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.chat_request import ChatRequest
from schemas.response_schema import APIResponse
from services.chat_message_service import ChatMessageService
from services.chat_service import ChatService

router = APIRouter(
    prefix="/chat-messages",
    tags=["Chat Messages"],
)

@router.get("/session/{session_id}", response_model=APIResponse)
def get_chat_history(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    chat_service = ChatService(db)

    session = chat_service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)
    message_service = ChatMessageService(db)
    messages = message_service.history(session.id)

    return success( messages, "Chat messages retrieved successfully.")

@router.get("/session/{session_id}/latest", response_model=APIResponse)
def get_latest_chat_message(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    chat_service = ChatService(db)

    session = chat_service.get_for_tenant( session_id=session_id, tenant_id=current_user.current_tenant_id)
    message_service = ChatMessageService(db)
    message = message_service.latest(session.id)

    return success(message, "Latest chat message retrieved successfully.")

@router.post("", response_model=APIResponse)
def create_user_message(payload: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    chat_service = ChatService(db)

    if payload.session_id is None:
        session = chat_service.create_for_tenant(
            actor_id=current_user.id,
            tenant_id=current_user.current_tenant_id,
            dataset_id=payload.dataset_id,
        )
    else:
        session = chat_service.get_for_tenant( session_id=payload.session_id, tenant_id=current_user.current_tenant_id)

        if session.dataset_id != payload.dataset_id:
            return success(None, "Chat session does not belong to the specified dataset.")

    message_service = ChatMessageService(db)
    message = message_service.add_user(actor_id=current_user.id, session=session, content=payload.message)

    return success(message, "Chat message created successfully.")

@router.get("/{message_id}", response_model=APIResponse)
def get_chat_message(message_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    message_service = ChatMessageService(db)
    chat_service = ChatService(db)

    message = message_service.get(message_id)
    chat_service.get_for_tenant(session_id=message.chat_session_id, tenant_id=current_user.current_tenant_id)

    return success(message, "Chat message retrieved successfully.")


@router.delete("/{message_id}", response_model=APIResponse)
def delete_chat_message(message_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    message_service = ChatMessageService(db)
    chat_service = ChatService(db)

    message = message_service.get(message_id)
    chat_service.get_for_tenant( session_id=message.chat_session_id, tenant_id=current_user.current_tenant_id)
    message_service.delete(actor_id=current_user.id, message=message)

    return success( None, "Chat message deleted successfully.")