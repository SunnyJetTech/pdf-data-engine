from __future__ import annotations
import hashlib
import hmac
import time
from typing import Any
from urllib.parse import quote
import requests
from core.config import settings
from payment.money import normalize_currency, to_minor_units

class StripeService:
    BASE_URL = "https://api.stripe.com/v1"

    @staticmethod
    def _secret() -> str:
        return settings.STRIPE_SECRET_KEY.get_secret_value()

    @classmethod
    def _headers(cls) -> dict[str, str]:
        return {"Authorization": f"Bearer {cls._secret()}"}

    @classmethod
    def initialize_payment(cls, *, email: str, amount: int, currency: str, reference: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        code = normalize_currency(currency)
        amount_minor = to_minor_units(amount, code)

        payload: dict[str, Any] = {
            "mode": "payment",
            "customer_email": email,
            "client_reference_id": reference,
            "success_url": settings.STRIPE_CALLBACK_URL,
            "cancel_url": settings.STRIPE_CANCEL_URL,
            "line_items[0][price_data][currency]": code.lower(),
            "line_items[0][price_data][unit_amount]": str(amount_minor),
            "line_items[0][price_data][product_data][name]": ("DataSage subscription"),
            "line_items[0][quantity]": "1",
            "metadata[reference]": reference,
        }

        for key, value in (metadata or {}).items():
            if value is not None:
                payload[f"metadata[{key}]"] = str(value)

        try:
            response = requests.post(f"{cls.BASE_URL}/checkout/sessions", data=payload, headers=cls._headers(), timeout=30)
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError) as exc:
            raise ValueError("Unable to initialize Stripe payment.") from exc

        if not result.get("id") or not result.get("url"):
            raise ValueError("Stripe did not return a valid Checkout Session.")

        return result

    @classmethod
    def verify_payment(cls, *, session_id: str) -> dict[str, Any]:
        encoded_id = quote(session_id, safe="")

        try:
            response = requests.get(
                f"{cls.BASE_URL}/checkout/sessions/{encoded_id}",
                params={"expand[]": "payment_intent"},
                headers=cls._headers(),
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError) as exc:
            raise ValueError("Unable to verify Stripe payment.") from exc

        return result

    @staticmethod
    def payment_successful(response: dict[str, Any]) -> bool:
        return (response.get("status") == "complete" and response.get("payment_status") == "paid")

    @classmethod
    def verify_signature(cls, *, payload: bytes, signature_header: str, tolerance_seconds: int = 300) -> bool:
        secret = settings.STRIPE_WEBHOOK_SECRET.get_secret_value()

        timestamp: int | None = None
        signatures: list[str] = []

        for item in signature_header.split(","):
            key, separator, value = item.strip().partition("=")

            if not separator:
                continue

            if key == "t":
                try:
                    timestamp = int(value)
                except ValueError:
                    return False
            elif key == "v1":
                signatures.append(value)

        if timestamp is None or not signatures:
            return False

        if abs(time.time() - timestamp) > tolerance_seconds:
            return False

        signed_payload = str(timestamp).encode() + b"." + payload
        expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()

        return any( hmac.compare_digest(expected, candidate) for candidate in signatures)

    @staticmethod
    def transaction_id(response: dict[str, Any]) -> str:
        intent = response.get("payment_intent")

        if isinstance(intent, dict):
            intent = intent.get("id")

        return str(intent or response.get("id") or "")
