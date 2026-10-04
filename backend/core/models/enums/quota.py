from enum import Enum

class QuotaType(str, Enum):

    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"