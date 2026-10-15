from __future__ import annotations
import hashlib
import hmac
from typing import Any
from urllib.parse import quote
import requests
from core.config import settings
from payment.money import normalize_currency, to_minor_units,

class PaystackService:
    BASE_URL = "https://api.paystack.co"

    @staticmethod
    def _secret() -> str:
        return settings.PAYSTACK_SECRET_KEY.get_secret_value()

    @classmethod
    def _headers(cls) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {cls._secret()}",
            "Content-Type": "application/json",
        }

    @classmethod
    def initialize_payment(cls, *, email: str, amount: int, currency: str, reference: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        code = normalize_currency(currency)

        payload: dict[str, Any] = {
            "email": email,
            "amount": to_minor_units(amount, code),
            "currency": code,
            "reference": reference,
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
            "metadata": metadata or {},
        }

        try:
            response = requests.post(f"{cls.BASE_URL}/transaction/initialize", json=payload, headers=cls._headers(), timeout=30)
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError) as exc:
            raise ValueError("Unable to initialize Paystack payment.") from exc

        if not result.get("status"):
            raise ValueError("Paystack rejected payment initialization.")

        return result

    @classmethod
    def verify_payment(cls, *, reference: str) -> dict[str, Any]:
        encoded_reference = quote(reference, safe="")

        try:
            response = requests.get(
                f"{cls.BASE_URL}/transaction/verify/{encoded_reference}",
                headers=cls._headers(),
                timeout=30,
            )
            
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError) as exc:
            raise ValueError(
                "Unable to verify Paystack payment."
            ) from exc

        if not result.get("status"):
            raise ValueError("Paystack could not verify the payment.")

        return result

    @classmethod
    def verify_signature(cls, *, payload: bytes, signature: str) -> bool:
        expected = hmac.new(cls._secret().encode("utf-8"), payload, hashlib.sha512).hexdigest()

        return hmac.compare_digest(expected, signature)

    @staticmethod
    def payment_successful(response: dict[str, Any]) -> bool:
        return (response.get("status") is True and response.get("data", {}).get("status") == "success")

    @staticmethod
    def authorization_url(response: dict[str, Any]) -> str:
        url = response.get("data", {}).get("authorization_url")

        if not isinstance(url, str) or not url:
            raise ValueError("Paystack did not return a checkout URL.")

        return url
