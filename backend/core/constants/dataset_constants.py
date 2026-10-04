from __future__ import annotations
from enum import Enum

class DatasetStatus(str, Enum):

    READY = "READY"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"

MAX_DATASET_ROWS = 1_000_000
MAX_DATASET_COLUMNS = 500
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500
DEFAULT_DATASET_NAME = "Untitled Dataset"