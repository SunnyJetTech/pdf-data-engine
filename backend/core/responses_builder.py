from typing import Any, TypeVar
from schema.response_schema import APIResponse

T = TypeVar("T")

def success(data: T | None = None, message: str = "Success") -> APIResponse[T]:

    return APIResponse[T](
        status="success",
        message=message,
        data=data,
    )

def created(data: T | None = None, message: str = "Created successfully") -> APIResponse[T]:

    return APIResponse[T](
        status="success",
        message=message,
        data=data,
    )

def failed(message: str, data: Any = None) -> APIResponse[Any]:

    return APIResponse[Any](
        status="failed",
        message=message,
        data=data,
    )

def paginated(*, items: list[Any], total: int, page: int, page_size: int, message: str = "Success") -> APIResponse[dict]:

    return APIResponse(
        status="success",
        message=message,
        data={
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": (total + page_size - 1) // page_size,
            },
        },
    )


def metadata(*, data: Any, meta: dict, message: str = "Success") -> APIResponse[dict]:

    return APIResponse(
        status="success",
        message=message,
        data={
            "data": data,
            "meta": meta,
        },
    )