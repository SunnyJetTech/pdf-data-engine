from __future__ import annotations
from fastapi import APIRouter, Cookie, Depends, Request, Response
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from db.database import get_db
from schemas.response_schema import APIResponse
from schemas.user_schema import ChangePasswordRequest, ForgotPasswordRequest, LoginRequest, ResetPasswordRequest
from core.responses_builder import success
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/login", response_model=APIResponse)
def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)

    result = service.login(
        response=response,
        email=payload.email,
        password=payload.password,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    return success(result, "Login successful.")

@router.post("/logout", response_model=APIResponse)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    result = service.logout(response=response, current_user=current_user, refresh_token=refresh_token)

    return success(message=result["message"])


@router.post("/refresh", response_model=APIResponse)
def refresh_access_token(response: Response, refresh_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    
    if refresh_token is None:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is required.")

    service = AuthService(db)
    result = service.refresh_access_token(response=response, refresh_token=refresh_token)

    return success(result, "Access token refreshed successfully.")


@router.post("/change-password", response_model=APIResponse)
def change_password(payload: ChangePasswordRequest, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = AuthService(db)
    result = service.change_password(current_user=current_user, current_password=payload.current_password, new_password=payload.new_password)

    return success(message=result["message"])

@router.post("/forgot-password", response_model=APIResponse)
async def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    await service.forgot_password(email=payload.email)

    return success(message="If the account exists, a password reset link has been sent.")

@router.post("/reset-password/{token}", response_model=APIResponse)
def reset_password( token: str, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    result = service.reset_password( token=token, new_password=payload.new_password)

    return success(message=result["message"])

@router.post("/verify-email/{token}", response_model=APIResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    result = service.verify_email(token=token)

    return success(message=result["message"])

@router.post("/resend-verification", response_model=APIResponse)
async def resend_verification(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = AuthService(db)
    await service.send_verification_email(user=current_user)

    return success(message="Verification email sent successfully.")

@router.post("/revoke-sessions", response_model=APIResponse)
def revoke_sessions(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    service = AuthService(db)
    service.revoke_sessions(current_user=current_user)

    return success(message="All active sessions have been revoked.")