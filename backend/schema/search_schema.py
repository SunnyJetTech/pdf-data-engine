from pydantic import BaseModel
from enum import Enum

class SearchOperator(str, Enum):
    EQUAL = "="
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="

class SearchRequest(BaseModel):
    document_id: int
    column: str
    operator: SearchOperator
    value: str
    page: int = 1
    page_size: int = 50