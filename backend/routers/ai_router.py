from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from db.database import get_db
from services.ai.ai_service import AIService
from services.dataset_service import DatasetService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

class ChatRequest(BaseModel):
    dataset_id: UUID
    question: str = Field(..., min_length=1)
    session_id: UUID | None = None

def _get_dataset(*, db: Session, current_user: User, dataset_id: UUID):
    dataset = DatasetService(db).get(dataset_id)

    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

    if dataset.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Dataset does not belong to your workspace.")

    return dataset

def _get_session(*, db: Session, current_user: User, session_id: UUID):
    ai = AIService(db)
    session = ai.chat.get(session_id)

    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found.")

    if session.dataset.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    return ai, session

@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    dataset = _get_dataset(db=db, current_user=current_user, dataset_id=request.dataset_id)

    ai = AIService(db)

    return await ai.chat( user=current_user, dataset=dataset, question=request.question, session_id=request.session_id)

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    dataset = _get_dataset(db=db, current_user=current_user, dataset_id=request.dataset_id)
    ai = AIService(db)

    stream = ai.chat_stream( user=current_user, dataset=dataset, question=request.question, session_id=request.session_id)

    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@router.get("/sessions/{dataset_id}")
def sessions(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    dataset = _get_dataset(db=db, current_user=current_user, dataset_id=dataset_id)
    ai = AIService(db)

    return ai.chat.by_dataset(dataset.id)

@router.get("/messages/{session_id}")
def messages(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    ai, _session = _get_session(db=db, current_user=current_user, session_id=session_id)

    return ai.messages.history(session_id)
