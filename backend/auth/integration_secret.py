from __future__ import annotations
from cryptography.fernet import Fernet, InvalidToken
from core.config import settings

class IntegrationSecretManager:

    @staticmethod
    def _fernet() -> Fernet:
        key = settings.WEBHOOK_ENCRYPTION_KEY

        if not key:
            raise RuntimeError("WEBHOOK_ENCRYPTION_KEY is not configured.")

        return Fernet(key)

    @classmethod
    def encrypt(cls, secret: str) -> str:
        return cls._fernet().encrypt(secret.encode("utf-8")).decode("utf-8")

    @classmethod
    def decrypt(cls, encrypted_secret: str) -> str:
        try:
            return cls._fernet().decrypt(encrypted_secret.encode("utf-8")).decode("utf-8")
        except InvalidToken as exc:
            raise RuntimeError("Unable to decrypt integration secret.") from exc