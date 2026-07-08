from __future__ import annotations
from datetime import timedelta
from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from auth.jwt_handler import create_access_token, create_password_reset_token, verify_password_reset_token
from auth.password_manager import password_hash, verify_password
from core.config import settings
from core.constants.activity import ActivityAction
from core.models import User
from services.activity_service import ActivityService
from services.mail_service import MailService


class AuthService:

    @classmethod
    def login(cls, *, db: Session, response: Response, email: str, password: str) -> dict:

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            }
        )

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24,
        )

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.LOGIN)

        return {
            "access_token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            },
        }

    @classmethod
    def logout(cls, *, db: Session, response: Response, user: User,):

        response.delete_cookie("access_token")

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.LOGOUT)


    @classmethod
    def change_password(cls, *, db: Session, user: User, current_password: str, new_password: str):

        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect.")

        user.password_hash = password_hash(new_password)

        db.commit()

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.PASSWORD_RESET)

    @classmethod
    async def forgot_password(cls, *, db: Session, email: str):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return

        expires = timedelta(minutes=30)

        token = create_password_reset_token({"email": user.email}, expires_delta=expires)

        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password/{token}"

        await MailService.send_password_reset_email(
            recipient=user.email,
            username=user.username,
            reset_url=reset_url,
        )

    @classmethod
    def reset_password(cls, *, db: Session, token: str, password: str):

        payload = verify_password_reset_token(token)

        email = payload.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Invalid token.")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user.password_hash = password_hash(password)

        db.commit()

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.PASSWORD_RESET)