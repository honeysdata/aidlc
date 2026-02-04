from pydantic import BaseModel
from typing import TypeVar, Generic, Any

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: T


class ErrorResponse(BaseModel):
    status: str = "error"
    code: str
    message: str
    details: dict[str, Any] | None = None


class MessageResponse(BaseModel):
    status: str = "success"
    message: str
