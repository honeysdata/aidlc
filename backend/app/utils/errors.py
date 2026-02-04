from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    content = {
        "status": "error",
        "code": exc.code,
        "message": exc.message
    }
    if exc.details:
        content["details"] = exc.details
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )


# Predefined exceptions
class NotFoundException(AppException):
    def __init__(self, resource: str, details: Optional[Dict] = None):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource}을(를) 찾을 수 없습니다",
            status_code=404,
            details=details
        )


class AuthenticationException(AppException):
    def __init__(self, message: str = "인증에 실패했습니다"):
        super().__init__(
            code="AUTH_FAILED",
            message=message,
            status_code=401
        )


class ValidationException(AppException):
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=400,
            details=details
        )


class BusinessRuleException(AppException):
    def __init__(self, code: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            code=code,
            message=message,
            status_code=422,
            details=details
        )
