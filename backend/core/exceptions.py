from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from schema.response_schema import APIResponse

class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code

class DocumentNotFound(AppException):
    def __init__(self):
        super().__init__(
            "Document not found",
            status.HTTP_404_NOT_FOUND,
        )

class SearchHistoryNotFound(AppException):
    def __init__(self):
        super().__init__(
            "Search history not found",
            status.HTTP_404_NOT_FOUND,
        )

class UserNotFound(AppException):
    def __init__(self):
        super().__init__(
            "User not found",
            status.HTTP_404_NOT_FOUND,
        )

class InvalidSearchOperator(AppException):
    def __init__(self):
        super().__init__(
            "Invalid search operator",
            status.HTTP_400_BAD_REQUEST,
        )

class FileTooLarge(AppException):
    def __init__(self):
        super().__init__(
            "Uploaded file exceeds allowed size",
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        )

class Unauthorized(AppException):
    def __init__(self):
        super().__init__(
            "Unauthorized",
            status.HTTP_401_UNAUTHORIZED,
        )

class Forbidden(AppException):
    def __init__(self):
        super().__init__(
            "Permission denied",
            status.HTTP_403_FORBIDDEN,
        )

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            status="failed",
            message=exc.message,
            data=None,
        ).model_dump(),
    )

async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=APIResponse(
            status="failed",
            message=str(exc),
            data=None,
        ).model_dump(),
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            status="failed",
            message=str(exc.detail),
            data=None,
        ).model_dump(),
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            status="failed",
            message="Internal server error",
            data=None,
        ).model_dump(),
    )