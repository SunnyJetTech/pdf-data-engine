from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.dependencies.search import get_saved_search_service
from schemas.saved_search.create_request import SavedSearchCreateRequest
from schemas.saved_search.response import SavedSearchResponse
from services.search.saved_search_service import SavedSearchService

router = APIRouter(
    prefix="/saved-searches",
    tags=["Saved Searches"],
)

@router.get("", response_model=list[SavedSearchResponse])
async def list_saved_searches(
    service: SavedSearchService = Depends(get_saved_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    return await service.list(user=current_user)

@router.get("/{search_id}", response_model=SavedSearchResponse)
async def get_saved_search(
    search_id: UUID,
    service: SavedSearchService = Depends(get_saved_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    search = await service.get(search_id=search_id, user=current_user)

    if search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved search not found.")

    return search

@router.post("", response_model=SavedSearchResponse, status_code=status.HTTP_201_CREATED)
async def create_saved_search(
    request: SavedSearchCreateRequest,
    service: SavedSearchService = Depends(get_saved_search_service),
    current_user: User = Depends(get_current_user_from_cookie),
):

    return await service.create(user=current_user, request=request)

@router.delete("/{search_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_search(

    search_id: UUID,

    service: SavedSearchService = Depends(
        get_saved_search_service,
    ),

    current_user: User = Depends(
        get_current_user_from_cookie,
    ),

):

    await service.delete(

        search_id=search_id,

        user=current_user,

    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )