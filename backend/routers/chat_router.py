from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status,
from core.auth import get_current_user_from_cookie
from core.dependencies.ai import get_ai_service
from core.dependencies.dataset import get_dataset_service
from core.models.user import User
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from services.ai.ai_service import AIService
from backend.services.dataset_service import DatasetService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest, ai: AIService = Depends(get_ai_service),
    datasets: DatasetService = Depends(get_dataset_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    dataset = datasets.get_ready(request.dataset_id)

    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found.")

    return await ai.chat(user=current_user, dataset=dataset, question=request.message, session_id=request.session_id)