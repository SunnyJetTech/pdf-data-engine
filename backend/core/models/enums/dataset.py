from enum import Enum

class DatasetStatus(str, Enum):

    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class DatasetVisibility(str, Enum):

    PRIVATE = "private"
    SHARED = "shared"
    PUBLIC = "public"