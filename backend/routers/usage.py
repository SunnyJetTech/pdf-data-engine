from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.usage_service import UsageService

router = APIRouter(
    prefix="/usage",
    tags=["Usage"],
)

@router.get("/current", response_model=APIResponse)
def get_current_usage(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = UsageService(db)
    usage = service.get(current_user.current_tenant_id)

    return success(usage, "Usage retrieved successfully.")