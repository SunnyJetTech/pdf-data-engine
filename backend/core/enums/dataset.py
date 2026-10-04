from enum import Enum

class DatasetStatus(str, Enum):
    READY = "READY"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"