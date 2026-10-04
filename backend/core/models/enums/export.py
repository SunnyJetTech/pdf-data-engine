from enum import Enum

class ExportType(str, Enum):

    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"

class ExportStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"