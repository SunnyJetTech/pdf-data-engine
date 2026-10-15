from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from db.database import get_db
from schemas.response_schema import APIResponse
from schemas.user_schema import ChangePasswordRequest
from core.responses_builder import success
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=APIResponse)
def get_current_user(current_user: User = Depends(get_current_user_from_cookie),):
    
    return success(current_user, "User profile retrieved successfully.")

@router.get("/{user_id}", response_model=APIResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = UserService(db)
    user = service.by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return success(user, "User retrieved successfully.")

@router.post("/me/change-password", response_model=APIResponse)
def change_password(payload: ChangePasswordRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = UserService(db)

    user = service.change_password(user=current_user, new_password=payload.new_password)

    db.commit()
    db.refresh(user)

    return success(user, "Password updated successfully.")