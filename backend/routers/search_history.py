from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schema.response_schema import APIResponse
from services.search_service import SearchService

router = APIRouter(
    prefix="/search-history",
    tags=["Search History"],
)

@router.get("", response_model=APIResponse)
def get_search_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SearchService(db)
    history = service.history_for_user(user_id=current_user.id)

    return success(history, "Search history retrieved successfully.")

@router.delete("", response_model=APIResponse)
def clear_search_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = SearchService(db)

    deleted_count = service.clear_history(user_id=current_user.id)

    return success({"deleted_count": deleted_count}, "Search history cleared successfully.")