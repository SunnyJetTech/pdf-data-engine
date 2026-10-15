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
from services.chat_service import ChatService

router = APIRouter(
    prefix="/chat-sessions",
    tags=["Chat Sessions"],
)

@router.get("", response_model=APIResponse)
def list_chat_sessions(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    sessions = service.by_dataset_for_tenant(dataset_id=dataset_id, tenant_id=current_user.current_tenant_id)

    return success(sessions, "Chat sessions retrieved successfully.")


@router.get("/latest", response_model=APIResponse)
def get_latest_chat_session(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    service.by_dataset_for_tenant(dataset_id=dataset_id, tenant_id=current_user.current_tenant_id)
    session = service.latest(dataset_id)

    return success(session, "Latest chat session retrieved successfully.")

@router.get("/active", response_model=APIResponse)
def get_active_chat_sessions(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    service.by_dataset_for_tenant(dataset_id=dataset_id, tenant_id=current_user.current_tenant_id)
    sessions = service.active(dataset_id)

    return success(sessions, "Active chat sessions retrieved successfully.")

@router.get("/pinned", response_model=APIResponse)
def get_pinned_chat_sessions(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    service.by_dataset_for_tenant(dataset_id=dataset_id, tenant_id=current_user.current_tenant_id)
    sessions = service.pinned(dataset_id)

    return success(sessions, "Pinned chat sessions retrieved successfully.")

@router.post("", response_model=APIResponse)
def create_chat_session(payload: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.create_for_tenant( actor_id=current_user.id, tenant_id=current_user.current_tenant_id, dataset_id=payload.dataset_id, title=None)

    return success(session, "Chat session created successfully.")

@router.get("/{session_id}", response_model=APIResponse)
def get_chat_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)

    return success(session, "Chat session retrieved successfully.",)

@router.get("/{session_id}/messages", response_model=APIResponse)
def get_chat_session_messages(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)

    return success(session.messages, "Chat session messages retrieved successfully.")

@router.patch("/{session_id}", response_model=APIResponse)
def rename_chat_session(session_id: UUID, title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant( session_id=session_id, tenant_id=current_user.current_tenant_id)
    updated = service.rename( session=session, title=title)

    return success( updated, "Chat session renamed successfully.")

@router.post("/{session_id}/pin", response_model=APIResponse)
def pin_chat_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)
    updated = service.pin(session)

    return success(updated, "Chat session pinned successfully.")

@router.post("/{session_id}/unpin", response_model=APIResponse)
def unpin_chat_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)
    updated = service.unpin(session)

    return success(updated, "Chat session unpinned successfully.")

@router.post("/{session_id}/archive", response_model=APIResponse)
def archive_chat_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)
    updated = service.archive(session)

    return success(updated, "Chat session archived successfully.")

@router.post("/{session_id}/activate", response_model=APIResponse)
def activate_chat_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant( session_id=session_id, tenant_id=current_user.current_tenant_id)
    updated = service.activate(session)

    return success(updated, "Chat session activated successfully.")

@router.delete("/{session_id}", response_model=APIResponse)
def delete_chat_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = ChatService(db)

    session = service.get_for_tenant(session_id=session_id, tenant_id=current_user.current_tenant_id)
    service.delete(actor_id=current_user.id, session=session)

    return success(None, "Chat session deleted successfully.")