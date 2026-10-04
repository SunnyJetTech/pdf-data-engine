from enum import StrEnum

class TenantStatus(StrEnum):
    ACTIVE = "active"
    TRIAL = "trial"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"