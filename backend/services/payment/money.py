from __future__ import annotations
from decimal import Decimal, InvalidOperation

ZERO_DECIMAL_CURRENCIES = {
    "BIF", "CLP", "DJF", "GNF", "ISK", "JPY",
    "KMF", "KRW", "PYG", "RWF", "UGX", "VND",
    "VUV", "XAF", "XOF", "XPF",
}

def normalize_currency(currency: str) -> str:
    normalized = currency.strip().upper()

    if len(normalized) != 3 or not normalized.isalpha():
        raise ValueError("Invalid currency code.")

    return normalized

def to_decimal_amount(amount: int | float | str | Decimal) -> Decimal:
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid payment amount.") from None

    if not value.is_finite() or value <= 0:
        raise ValueError("Payment amount must be positive and finite.")

    return value

def to_minor_units(amount: int | float | str | Decimal, currency: str) -> int:
    value = to_decimal_amount(amount)
    code = normalize_currency(currency)
    exponent = 0 if code in ZERO_DECIMAL_CURRENCIES else 2
    multiplier = Decimal(10) ** exponent
    scaled = value * multiplier

    if scaled != scaled.to_integral_value():
        raise ValueError(f"Amount has too many decimal places for {code}.")

    return int(scaled)
