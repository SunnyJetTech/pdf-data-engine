from __future__ import annotations
import hmac
from decimal import Decimal
from typing import Any
from urllib.parse import quote
import requests
from core.config import settings
from payment.money import normalize_currency, to_decimal_amount

class FlutterwaveService:
    BASE_URL = "https://api.flutterwave.com/v3"

    @staticmethod
    def _secret() -> str:
        return settings.FLUTTERWAVE_SECRET_KEY.get_secret_value()

    @classmethod
    def _headers(cls) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {cls._secret()}",
            "Content-Type": "application/json",
        }

    @classmethod
    def initialize_payment(cls, *, email: str, amount: int, currency: str, reference: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        code = normalize_currency(currency)
        value = to_decimal_amount(amount)

        payload = {
            "tx_ref": reference,
            "amount": format(value, "f"),
            "currency": code,
            "redirect_url": settings.FLUTTERWAVE_CALLBACK_URL,
            "customer": {"email": email},
            "meta": metadata or {},
            "customizations": {"title": "DataSage subscription", "description": "Subscription payment"},
        }

        try:
            response = requests.post(f"{cls.BASE_URL}/payments", json=payload, headers=cls._headers(), timeout=30)
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError) as exc:
            raise ValueError("Unable to initialize Flutterwave payment.") from exc

        if result.get("status") != "success":
            raise ValueError("Flutterwave rejected payment initialization.")

        link = result.get("data", {}).get("link")

        if not isinstance(link, str) or not link:
            raise ValueError("Flutterwave did not return a checkout URL.")

        return result

    @classmethod
    def verify_payment(cls, *, transaction_id: str) -> dict[str, Any]:
        encoded_id = quote(transaction_id, safe="")

        try:
            response = requests.get(f"{cls.BASE_URL}/transactions/{encoded_id}/verify", headers=cls._headers(), timeout=30)
            
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError) as exc:
            raise ValueError("Unable to verify Flutterwave payment.") from exc

        if result.get("status") != "success":
            raise ValueError("Flutterwave could not verify the payment.")

        return result

    @staticmethod
    def payment_successful(response: dict[str, Any]) -> bool:
        return (response.get("status") == "success" and response.get("data", {}).get("status") == "successful")

    @staticmethod
    def verify_signature(*, signature: str) -> bool:
        expected = (settings.FLUTTERWAVE_WEBHOOK_SECRET.get_secret_value())

        return hmac.compare_digest(expected, signature)

    @staticmethod
    def transaction_data(response: dict[str, Any]) -> dict[str, Any]:
        return response.get("data", {})
