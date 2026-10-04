from __future__ import annotations
from datetime import timedelta
from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from auth.jwt_handler import create_access_token, create_password_reset_token, decode_token, verify_password_reset_token,
from auth.password_manager import password_hash, verify_password
from core.config import settings
from core.constants.activity import ActivityAction
from core.models.user import User
from repositories.user_repository import UserRepository
from services.activity_service import ActivityService
from services.mail_service import MailService
from services.refresh_token_service import RefreshTokenService

class AuthService:
    def __init__(self, db: Session) -> None:
            self.db = db
            self.users = UserRepository(db)
            self.refresh_tokens = RefreshTokenService(db)
            self.activity = ActivityService(db)

    def _set_access_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def _set_refresh_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(
            key="refresh_token",
            value=token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        )

    def _clear_cookies(self, response: Response) -> None:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    def _access_claims(self, user: User) -> dict:
        return {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
            "tenant_id": ( str(user.current_tenant_id) if user.current_tenant_id else None),
            "is_superuser": user.is_superuser,
        }

    def authenticate( self, *, email: str, password: str) -> User:
        user = self.users.by_email(email=email)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account has been disabled.")

        return user

    def login(self, *, response: Response, email: str, password: str, ip_address: str | None = None, user_agent: str | None = None) -> dict:
        user = self.authenticate(email=email, password=password)
        access_token = create_access_token(self._access_claims(user))
        refresh_token = self.refresh_tokens.create( user_id=user.id, ip_address=ip_address, user_agent=user_agent)

        self._set_access_cookie(response, access_token)
        self._set_refresh_cookie( response, refresh_token)

        self.activity.log( user_id=user.id, action=ActivityAction.LOGIN)
        self.db.commit()

        return {
            "message": "Login successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }

    def logout(self, *, response: Response, current_user: User, refresh_token: str | None = None) -> dict:
        if refresh_token:
            try:
                self.refresh_tokens.revoke(refresh_token=refresh_token)
            except HTTPException:
                pass

        self._clear_cookies(response)

        self.activity.log(user_id=current_user.id, action=ActivityAction.LOGOUT)

        self.db.commit()

        return {
            "message": "Logout successful.",
        }

    def refresh_access_token(self, *, response: Response, refresh_token: str) -> dict:
        new_refresh_token, new_plaintext = (self.refresh_tokens.rotate(refresh_token=refresh_token))
        user = self.users.by_id(new_refresh_token.user_id)

        if user is None:
            self.db.rollback()

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        if not user.is_active:
            self.db.rollback()

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account has been disabled.")

        access_token = create_access_token(self._access_claims(user))

        self._set_access_cookie(response, access_token)
        self._set_refresh_cookie(response, new_plaintext)

        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_plaintext,
        }

    def change_password(self, *, current_user: User, current_password: str, new_password: str) -> dict:
        if not verify_password(current_password, current_user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect.")

        current_user.password_hash = password_hash(new_password)

        self.activity.log(user_id=current_user.id, action=ActivityAction.PASSWORD_CHANGED)

        self.db.commit()

        return {
            "message": "Password updated successfully.",
        }

    async def forgot_password(self, *, email: str) -> None:
        user = self.users.by_email(email=email)

        if user is None:
            return

        token = create_password_reset_token(
            {
                "sub": str(user.id),
                "email": user.email,
            },
            expires_delta=timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES),
        )

        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password/{token}"   

        await MailService.send_password_reset_email(recipient=user.email, username=user.username, reset_url=reset_url)

        self.activity.log(user_id=user.id, action=ActivityAction.PASSWORD_RESET_REQUESTED)

        self.db.commit()

    def reset_password(self, *, token: str, new_password: str) -> dict:
        payload = verify_password_reset_token(token)

        user = self.users.by_email(email=payload["email"])

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        user.password_hash = password_hash(new_password)

        self.activity.log(user_id=user.id, action=ActivityAction.PASSWORD_RESET)

        self.db.commit()

        return {
            "message": "Password reset successful.",
        }

    async def send_verification_email(self, *, user: User) -> None:
        verification_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "type": "verify-email",
            },
            expires_delta=timedelta(hours=24),
        )

        verification_url = f"{settings.FRONTEND_BASE_URL}/verify-email/{verification_token}"

        await MailService.send_verification_email(recipient=user.email, username=user.username, verification_url=verification_url)

    def verify_email(self, *, token: str) -> dict:
        payload = decode_token(token)

        if payload.get("type") != "verify-email":
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification token.")

        user = self.users.by_email(email=payload["email"])

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        user.is_verified = True

        self.activity.log(user_id=user.id, action=ActivityAction.EMAIL_VERIFIED)

        self.db.commit()

        return {
            "message": "Email verified successfully.",
        }

    def revoke_sessions(self, *, current_user: User) -> None:
        self.refresh_tokens.revoke_user_sessions(user_id=current_user.id)

        self.activity.log(user_id=current_user.id, action=ActivityAction.SESSIONS_REVOKED)

        self.db.commit()