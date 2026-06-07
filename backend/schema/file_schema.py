from pydantic import BaseModel, model_validator
from fastapi import UploadFile, File
from typing import Any
from enum import Enum

class SaveMode(str, Enum):
    DATABASE = "database"
    EXCEL = "excel"
    NONE = "none"

class APIResponse(BaseModel):
    status: str
    message: str
    data: Any = None
        
    
