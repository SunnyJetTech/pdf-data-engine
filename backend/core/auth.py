from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from auth.jwt_handler import decode_token
from core.models.user import User
from db.database import get_db

def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db),):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    payload = decode_token(token)

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

def get_optional_user(request: Request, db: Session = Depends(get_db),):
    try:
        return get_current_user_from_cookie(request, db)
    except HTTPException:
        return None
    
def user_required(current_user: User = Depends(get_current_user_from_cookie),):
    return current_user

def admin_required(current_user: User = Depends(get_current_user_from_cookie)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Admin access required.",
        )

    return current_user