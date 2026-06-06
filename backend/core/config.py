from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_PREFIX: str = "/api/v1"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    SECRET_KEY: str = ''
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15

    POSTGRES_DATABASE_URL: str = ''
    MONGO_URL: str = ''
    MONGO_DATABASE: str = ''

    HOST: str = ''
    PORT: int = 8000
    
    FRONTEND_BASE_URL: str = ''
    BACKEND_BASE_URL: str = '' 

    ALLOWED_ORIGINS: str
    
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    @property
    def allowed_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()