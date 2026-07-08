import re
from typing import Any
from bson.regex import Regex

def _parse_value(value: str) -> Any:
    if isinstance(value, (int, float)):
        return value

    value = value.strip()

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def build_query(field_name: str, operator: str, value: str) -> dict:
    value = _parse_value(value)

    operators = {
        "=": lambda: {field_name: value},
        "!=": lambda: {field_name: {"$ne": value}},
        ">": lambda: {field_name: {"$gt": value}},
        "<": lambda: {field_name: {"$lt": value}},
        ">=": lambda: {field_name: {"$gte": value}},
        "<=": lambda: {field_name: {"$lte": value}},
        "contains": lambda: {field_name: Regex(re.escape(str(value)), "i")},
        "startswith": lambda: {field_name: Regex(f"^{re.escape(str(value))}", "i")},
        "endswith": lambda: {field_name: Regex(f"{re.escape(str(value))}$", "i")},
    }

    if operator not in operators:
        raise ValueError(
            f"Unsupported operator: {operator}"
        )

    return operators[operator]()