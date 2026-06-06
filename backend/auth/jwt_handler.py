from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from core.config import settings 
from core.Models import User 

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire, "type": "access"})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_password_reset_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire, "type": "password_reset"})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    payload.update({"exp": expire, "type": "refresh"})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def verify_access_token(token: str) -> dict:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    return payload

def verify_password_reset_token(token: str) -> dict:
    payload = decode_token(token)
    if payload.get("type") != "password_reset":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    return payload


def verify_refresh_token(token: str) -> dict:
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return payload

def get_user_id(payload: dict) -> int:
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing from token")

    return int(user_id)


def get_user_email(payload: dict) -> str:
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email missing from token")

    return email

def is_admin(payload: dict) -> bool:
    return payload.get("is_admin", False)

def require_admin(payload: dict) -> None:
    if not is_admin(payload):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: You do not have the necessary permissions")

def generate_new_access_token(refresh_token: str) -> str:
    payload = verify_refresh_token(refresh_token)
    return create_access_token(
        {
            "user_id": payload.get(
                "user_id"
            ),
            "email": payload.get(
                "email"
            ),
            "is_admin": payload.get(
                "is_admin",
                False
            )
        }
    )