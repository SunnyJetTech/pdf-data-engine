from __future__ import annotations
from enum import Enum

class SearchOperator(str, Enum):

    EQ = "="
    NE = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    IN = "in"
    NOT_IN = "not_in"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"

DEFAULT_SORT_DIRECTION = SortDirection.ASC