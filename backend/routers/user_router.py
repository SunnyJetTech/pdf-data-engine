from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from db.database import get_db
from core.auth import get_current_user_from_cookie, get_optional_user
from core.models import User
from services.user_service import UserService
from services.auth_service import AuthService
from schema.user_schema import UserRegister, LoginRequest, ChangePasswordRequest, ResetPasswordRequest, ForgotPasswordRequest
from schema.response_schema import APIResponse
from core.responses_builder import success

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)

@router.get("/me", response_model=APIResponse)
def current_user(user: User = Depends(get_current_user_from_cookie),):
    return success(UserService.serialize(user))

@router.get("/optional-me", response_model=APIResponse)
def optional_user(user: User | None = Depends(get_optional_user)):
    if not user:
        return success(None)

    return success(UserService.serialize(user))

@router.get("/admin-check", response_model=APIResponse)
def admin_check(user: User = Depends(get_current_user_from_cookie)):
    return success(UserService.admin_check(user))

@router.post("/register", response_model=APIResponse)
async def register(payload: UserRegister, db: Session = Depends(get_db)): 
    user = await UserService.register(db=db, payload=payload)

    return success(UserService.serialize(user), "User registered successfully")

@router.post("/login", response_model=APIResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    data = AuthService.login(db=db, response=response, email=payload.email, password=payload.password)

    return success(data, "Login successful")

@router.post("/logout", response_model=APIResponse)
def logout(response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    AuthService.logout(db=db, response=response, user=current_user)

    return success(message="Logged out successfully")

@router.post("/change-password", response_model=APIResponse)
def change_password(payload: ChangePasswordRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    AuthService.change_password(db=db, user=current_user, current_password=payload.current_password, new_password=payload.new_password)

    return success(message="Password changed successfully")

@router.post("/forgot-password", response_model=APIResponse)
async def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    await AuthService.forgot_password(db=db, email=payload.email)

    return success(message="If the account exists, a reset link has been sent.")

@router.post("/reset-password/{token}", response_model=APIResponse)
def reset_password(token: str, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    AuthService.reset_password(db=db, token=token, password=payload.password)

    return success(message="Password reset successfully")

@router.get("/profile", response_model=APIResponse)
def profile(current_user: User = Depends(get_current_user_from_cookie)):
    return success(UserService.serialize(current_user))