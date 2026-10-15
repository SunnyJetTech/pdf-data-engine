from __future__ import annotations
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

@router.post("", response_model=APIResponse)
async def search(
    dataset_id: UUID,
    query: Annotated[str, Query(min_length=1)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    service = SearchService(db)

    result = await service.search(user_id=current_user.id, tenant_id=current_user.current_tenant_id, dataset_id=dataset_id, query=query, limit=limit)

    return success(result, "Search completed successfully.")


@router.get("/context", response_model=APIResponse)
async def retrieve_context(
    dataset_id: UUID,
    query: Annotated[str, Query(min_length=1)],
    limit: Annotated[int, Query(ge=1, le=50)] = 8,
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    service = SearchService(db)

    context = await service.retrieve_context(tenant_id=current_user.current_tenant_id, dataset_id=dataset_id, query=query, limit=limit)

    return success(context, "Search context retrieved successfully.")


@router.get("/history", response_model=APIResponse)
def search_history(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = SearchService(db)

    history = service.history_for_user(user_id=current_user.id)

    return success(history, "Search history retrieved successfully.")


@router.delete("/history", response_model=APIResponse)
def clear_search_history(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = SearchService(db)

    deleted = service.clear_history(user_id=current_user.id)

    return success({"deleted_count": deleted}, "Search history cleared successfully.")


@router.get("/saved", response_model=APIResponse)
def saved_searches(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = SearchService(db)

    searches = service.saved_searches(user_id=current_user.id)

    return success(searches, "Saved searches retrieved successfully.")


@router.post("/saved", response_model=APIResponse)
def save_search(
    dataset_id: UUID,
    name: Annotated[str, Query(min_length=1, max_length=150)],
    query: Annotated[str, Query(min_length=1)],
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    service = SearchService(db)

    saved_search = service.save_search(
        user_id=current_user.id,
        tenant_id=current_user.current_tenant_id,
        dataset_id=dataset_id,
        name=name,
        query=query,
    )

    return success(saved_search, "Search saved successfully.")

@router.get("/saved/{search_id}", response_model=APIResponse)
def get_saved_search(search_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = SearchService(db)

    saved_search = service.get_saved_search(search_id=search_id, user_id=current_user.id)

    return success(saved_search, "Saved search retrieved successfully.") 

@router.delete("/saved/{search_id}", response_model=APIResponse)
def delete_saved_search(search_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = SearchService(db)

    service.delete_saved_search(search_id=search_id, user_id=current_user.id)

    return success(None, "Saved search deleted successfully.")