from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None


class PaginatedResponse(APIResponse[List[T]], Generic[T]):
    total: int
    skip: int
    limit: int


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None
