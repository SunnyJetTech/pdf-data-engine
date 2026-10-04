from __future__ import annotations
import hashlib
import hmac
from typing import Any
import requests
from core.config import settings

class PaystackService:

    BASE_URL = "https://api.paystack.co"

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

    @classmethod
    def initialize_payment(cls, *, email: str, amount: int, reference: str) -> dict[str, Any]:

        payload = {
            "email": email,
            "amount": amount,
            "reference": reference,
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/transaction/initialize",
                json=payload,
                headers=cls._headers(),
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as exc:
            raise ValueError(f"Unable to initialize payment: {exc}")

    @classmethod
    def verify_payment(cls, *, reference: str,) -> dict[str, Any]:
        try:
            response = requests.get(
                f"{cls.BASE_URL}/transaction/verify/{reference}",
                headers=cls._headers(),
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as exc:
            raise ValueError(f"Unable to verify payment: {exc}")

    @staticmethod
    def verify_signature(*, payload: bytes, signature: str) -> bool:
        computed_signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode(),
            payload,
            hashlib.sha512,
        ).hexdigest()

        return hmac.compare_digest(
            computed_signature,
            signature,
        )

    @staticmethod
    def payment_successful(response: dict[str, Any]) -> bool:
        if not response.get("status"):
            return False

        data = response.get("data", {})

        return data.get("status") == "success"

    @staticmethod
    def authorization_url(response: dict[str, Any]) -> str:

        return (
            response.get("data", {})
            .get("authorization_url", "")
        )