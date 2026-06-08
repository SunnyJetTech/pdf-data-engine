from fastapi import APIRouter, BackgroundTasks, Depends, Response
from db.database import get_db
from core.functions import (get_current_user_from_cookie, get_optional_user)
from auth.password_manager import password_hash, verify_password
from core.Models import User
from core.config import settings
from auth.jwt_handler import create_access_token
from datetime import timedelta
from services.mail_service import send_email
from sqlalchemy.orm import Session
from auth.jwt_handler import (
    decode_token, 
    get_user_email,
    create_password_reset_token,
    verify_password_reset_token
)
from schema.user_schema import (
    UserOut, 
    APIResponse, 
    OptionalUserResponse, 
    AdminCheckResponse, 
    UserIn, 
    LoginInputSchema,
    ChangePasswordSchema,
    ResetPasswordSchema,
)
router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me", response_model=APIResponse)
def read_current_user(user=Depends(get_current_user_from_cookie)):
    return APIResponse(
        status="success",
        data=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
        ).model_dump()
    )

@router.get("/optional-me", response_model=OptionalUserResponse)
def read_optional_user(user=Depends(get_optional_user)):
    if not user:
        return OptionalUserResponse(status="success", message="Guest user", data=None)

    return OptionalUserResponse(
        status="success",
        message="Logged in user",
        data=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            has_active_subscription=user.has_active_subscription,
            subscription_date=user.subscription_date,
            subscription_expiry=user.subscription_expiry,
        )
    )

@router.get("/admin-check", response_model=AdminCheckResponse)
def admin_check(user=Depends(get_current_user_from_cookie)):
    if not user.is_admin:
        return AdminCheckResponse(status="error", message="Access denied", data=None)

    return AdminCheckResponse(
        status="success",
        message="Admin verified",
        data={
            "user_id": user.id,
            "email": user.email
        }
    )
    
@router.post("/register", response_model=APIResponse)
async def register_user(user_data: UserIn, background_tasks: BackgroundTasks,  db=Depends(get_db)):
    try:
        user_data.validate_request()
    except ValueError as e:
        return APIResponse(status="error", message=str(e), data=None)
    
    existing_user = db.query(User).filter((User.email == user_data.email) | (User.username == user_data.username)).first()
    if existing_user:
        return APIResponse(status="error", message="User email/username already exists", data=None)

    password = user_data.password 
    user_data = user_data.model_dump(exclude=['confirm_password', 'password'], exclude_unset=True)
    user_data.update({
        "password_hash": password_hash(password),
        "is_active": True,
    })
    
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    background_tasks.add_task(send_email, recipient=user.email, subject="Welcome Message", body=f"Hi {user.username}, welcome to our platform!")

    return APIResponse(status="success", message="User registered successfully")

@router.post('/login', response_model=APIResponse)
def login(user_data: LoginInputSchema, response: Response, db = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        return APIResponse(status='failed', message="Invalid credentials", data={"email": user_data.email, "password": ''})
    
    token = create_access_token({'email': user.email, 'user_id':user.id, 'username': user.username, "is_admin": user.is_admin})
    response.set_cookie(
        key='access_token',
        value = token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=60*60*24
    )
    
    data = {
        "username": user.username,
        "email": user.email,
        "user_id": user.id,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "access_token": token
    }
    
    return APIResponse(
        status='success',
        message='Loggedin successfully',
        data = data
    )
    
@router.post('/logout', response_model=APIResponse)
def logout(response: Response, db = Depends(get_db)):
    response.delete_cookie('access_token')
    return APIResponse(
        status =  'success',
        message= "Logout successfully"
    )
    
@router.post('/change-password', response_model=APIResponse)
def change_password(payload: ChangePasswordSchema, db= Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    if not verify_password(payload.password, current_user.password_hash):
        return APIResponse(status="failed", message="Invalid Credential")
    
    try:
        payload.validate_password()
    except ValueError as e:
        return APIResponse(status="error", message=str(e), data=None)
    
    
    current_user.password_hash = password_hash(payload.new_password)
    db.commit()
    db.refresh(current_user)
    
    return APIResponse(
        status="success",
        message="Password changed successfully",
    )
    
@router.post("/forgot-password", response_model=APIResponse)
def forgot_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.email == email).first())

    if user:
        expires = timedelta(minutes=getattr(settings, "RESET_TOKEN_EXPIRE_MINUTES", 15))

        token = create_password_reset_token({"email": user.email}, expires_delta=expires)

        link = (f"{settings.FRONTEND_BASE_URL}"f"/reset-password/{token}")
        print(link)

        background_tasks.add_task(
            send_email,
            recipient=user.email,
            subject="Password Reset",
            body=f"Click the link below to reset your password:\n\n{link}"
        )

    return APIResponse(
        status="success",
        message="If the account exists, a reset link has been sent."
    )
    
@router.post("/reset-password/{token}", response_model=APIResponse)
def reset_password(token: str, payload: ResetPasswordSchema, db: Session = Depends(get_db)):
    try:
        payload.validate_password()
    except ValueError as e:
        return APIResponse(status="error", message=str(e), data=None)
    

    try:
        decoded = verify_password_reset_token(token)

        email = decoded.get("email")

        if not email:
            return APIResponse(status="failed", message="Invalid token")

        user = (db.query(User).filter(User.email == email).first())

        if not user:
            return APIResponse(status="failed", message="User not found")

    except Exception:
        return APIResponse(status="failed", message="Invalid or expired token")

    user.password_hash = password_hash(payload.password)

    db.commit()
    db.refresh(user)

    return APIResponse(status="success", message="Password reset successfully")