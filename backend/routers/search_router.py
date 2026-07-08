from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from core.auth import get_current_user_from_cookie
from core.models import User
from core.responses_builder import success
from schema.response_schema import APIResponse
from schema.search_schema import SearchRequest
from services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post("/", response_model=APIResponse)
def search_document(payload: SearchRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    result = SearchService.search(db=db, user_id=current_user.id, payload=payload)

    return success(
        data=result,
        message="Search completed successfully.",
    )


@router.get("/history", response_model=APIResponse)
def search_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    history = SearchService.get_history(db=db, user_id=current_user.id)

    return success(
        data=SearchService.serialize_history_many(history),
        message="Search history retrieved successfully.",
    )