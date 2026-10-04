from enum import Enum

class PaymentStatus(str, Enum):

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentProvider(str, Enum):

    PAYSTACK = "paystack"
    STRIPE = "stripe"