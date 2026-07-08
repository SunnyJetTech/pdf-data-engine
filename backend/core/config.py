from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    API_PREFIX: str = "/api/v1"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15

    POSTGRES_DATABASE_URL: str

    MONGO_URL: str
    MONGO_DATABASE: str

    FRONTEND_BASE_URL: str
    BACKEND_BASE_URL: str

    ALLOWED_ORIGINS: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: str

    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    PAYSTACK_SECRET_KEY: SecretStr
    PAYSTACK_PUBLIC_KEY: SecretStr
    PAYSTACK_CALLBACK_URL: str

    MAX_FREE_FILE_SIZE_MB: int = 20
    MAX_PRO_FILE_SIZE_MB: int = 100

    @property
    def allowed_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def max_free_file_size_bytes(self) -> int:
        return self.MAX_FREE_FILE_SIZE_MB * 1024 * 1024

    @property
    def max_pro_file_size_bytes(self) -> int:
        return self.MAX_PRO_FILE_SIZE_MB * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()