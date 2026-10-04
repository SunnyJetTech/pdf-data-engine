from __future__ import annotations
from math import ceil
from typing import Generic, Sequence, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class Pagination(BaseModel):

    page: int = 1
    page_size: int = 20
    model_config = ConfigDict(frozen=True)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class Page(BaseModel, Generic[T]):

    items: Sequence[T]

    total: int

    page: int

    page_size: int

    pages: int

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @classmethod
    def create(cls, *, items: Sequence[T], total: int, pagination: Pagination):

        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=max(
                ceil(total / pagination.page_size),
                1,
            ),
        )
        