from enum import Enum

class SubscriptionStatus(str, Enum):

    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"