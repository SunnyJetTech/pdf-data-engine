from enum import StrEnum

class PaymentStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentProvider(StrEnum):
    PAYSTACK = "paystack"
    STRIPE = "stripe"
    FLUTTERWAVE = "flutterwave"