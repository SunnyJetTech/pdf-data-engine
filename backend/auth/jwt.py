from jose import JWTError, jwt
from fastapi import HTTPException, status
from core.config import settings

class JWTService:

    @staticmethod
    def decode(token: str):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @staticmethod
    def verify_access(token: str):

        payload = JWTService.decode(token)

        if payload["type"] != "access":
            raise HTTPException(status_code=401, detail="Invalid access token")

        return payload

    @staticmethod
    def verify_refresh(token: str):

        payload = JWTService.decode(token)

        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return payload

    @staticmethod
    def verify_password_reset(token: str):

        payload = JWTService.decode(token)

        if payload["type"] != "password_reset":
            raise HTTPException(status_code=401, detail="Invalid reset token")

        return payload