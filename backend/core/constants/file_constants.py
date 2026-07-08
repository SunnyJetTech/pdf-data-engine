from enum import Enum

class SaveMode(str, Enum):
    DATABASE = "database"
    EXCEL = "excel"
    NONE = "none"