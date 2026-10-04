from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "DataSage"
    API_PREFIX: str = "/api/v1"
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Authentication
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15

    # Database
    POSTGRES_DATABASE_URL: str

    MONGO_URL: str
    MONGO_DATABASE: str

    # URLs
    FRONTEND_BASE_URL: str
    BACKEND_BASE_URL: str

    ALLOWED_ORIGINS: str

    # Mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: str

    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    # Payments
    PAYSTACK_SECRET_KEY: SecretStr
    PAYSTACK_PUBLIC_KEY: SecretStr
    PAYSTACK_CALLBACK_URL: str

    # File limits
    MAX_FREE_FILE_SIZE_MB: int = 20
    MAX_PRO_FILE_SIZE_MB: int = 100

    # AI
    OPENAI_API_KEY: SecretStr
    OPENAI_CHAT_MODEL: str = "gpt-4.1-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Redis / Background tasks
    REDIS_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    CELERY_TASK_ALWAYS_EAGER: bool = False
    CELERY_TASK_TIME_LIMIT: int = 3600
    CELERY_TASK_SOFT_TIME_LIMIT: int = 3300

    CELERY_RESULT_EXPIRES_SECONDS: int = 86400

    # Webhook security
    WEBHOOK_ENCRYPTION_KEY: SecretStr
    WEBHOOK_SIGNATURE_TOLERANCE_SECONDS: int = 300

    # API key security / lifecycle
    API_KEY_PREFIX: str = "ds_live_"

    # Middleware / API protection
    RATE_LIMIT_ENABLED: bool = True
    
    # AI
    OPENAI_API_KEY: SecretStr
    OPENAI_CHAT_MODEL: str = "gpt-4.1-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    GEMINI_API_KEY: SecretStr
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-2"
    GEMINI_EMBEDDING_DIMENSIONS: int = 768

    # Derived settings
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

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()