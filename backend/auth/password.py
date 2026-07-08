from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings

class TokenService:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        payload = data.copy()

        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        payload.update(
            {
                "exp": expire,
                "type": "access",
            }
        )

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
        payload = data.copy()

        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

        payload.update(
            {
                "exp": expire,
                "type": "refresh",
            }
        )

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def create_password_reset_token(
        data: dict,
        expires_delta: timedelta | None = None,
    ):
        payload = data.copy()

        expire = datetime.now(
            timezone.utc
        ) + (
            expires_delta
            or timedelta(minutes=15)
        )

        payload.update(
            {
                "exp": expire,
                "type": "password_reset",
            }
        )

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)