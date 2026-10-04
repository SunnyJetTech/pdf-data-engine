from pydantic import BaseModel

class DuplicateItem(BaseModel):
    value: str | int | float | None
    count: int
    rows: list[dict]


class DuplicateResponse(BaseModel):
    duplicates: list[DuplicateItem]