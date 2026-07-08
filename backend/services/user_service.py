from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.models import User
from core.config import settings
from auth.password_manager import password_hash, verify_password
from auth.jwt_handler import create_access_token, create_password_reset_token, verify_password_reset_token
from services.mail_service import MailService
from services.activity_service import ActivityService,ActivityAction


class UserService:

    @staticmethod
    def serialize(user: User) -> dict:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
        }

    @staticmethod
    async def register(*, db: Session, payload) -> User:

        existing = db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first()

        if existing:
            raise ValueError("Email or username already exists.")

        data = payload.model_dump(exclude={"password","confirm_password"})

        user = User(**data, password_hash=password_hash(payload.password), is_active=True)

        db.add(user)
        db.commit()
        db.refresh(user) 

        await MailService.send(recipient=user.email, subject="Welcome",
            body=f"""
            Hi {user.username},

            Welcome to our platform.

            Thank you for registering.
            """,
        )

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.USER_CREATED)

        return user

    @staticmethod
    def login(*, db: Session, email: str, password: str):

        user = db.query(User).filter(User.email == email).first()

        if (not user or not verify_password(password, user.password_hash)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            }
        )

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.LOGIN)

        return {
            "access_token": token,
            "user": UserService.serialize(user),
        }

    @staticmethod
    def logout(*, db: Session, user: User):

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.LOGOUT)

    @staticmethod
    def change_password(*, db: Session, current_user: User, old_password: str, new_password: str):

        if not verify_password(old_password, current_user.password_hash):
            raise ValueError("Invalid current password.")

        current_user.password_hash = password_hash(new_password)

        db.commit()

        ActivityService.log(db=db, user_id=current_user.id, action=ActivityAction.PASSWORD_RESET)

    @staticmethod
    async def forgot_password(*, db: Session, email: str):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return

        token = create_password_reset_token(
            {"email": user.email,},
            expires_delta=timedelta(minutes=15,),
        )

        link = (f"{settings.FRONTEND_BASE_URL}"f"/reset-password/{token}")

        await MailService.send_email(
            recipient=user.email,
            subject="Password Reset",
            body=f"""
            Click the link below to reset your password.

            {link}
            """,
        )

    @staticmethod
    def reset_password(*, db: Session, token: str, password: str):

        payload = verify_password_reset_token(token)

        email = payload.get("email")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise ValueError("User not found.")

        user.password_hash = password_hash(password)

        db.commit()

        ActivityService.log(db=db, user_id=user.id, action=ActivityAction.PASSWORD_RESET)

    @staticmethod
    def admin_check(user: User):

        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

        return {
            "user_id": user.id,
            "email": user.email,
        }