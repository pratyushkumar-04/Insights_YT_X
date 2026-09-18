"""Common schema objects used across the API."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error payload."""

    status: str = "error"
    error: str
    details: Optional[Dict[str, Any]] = None
    path: str
    request_id: Optional[str] = None
    timestamp: datetime


class HealthResponse(BaseModel):
    """Service health response."""

    status: str = "ok"
    app: str
    version: str
    environment: str
    timestamp: datetime


class Pagination(BaseModel):
    """Pagination metadata."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    total: int = 0
    total_pages: int = 0


class SuccessResponse(BaseModel):
    """Generic success payload."""

    status: str = "success"
    message: str
    data: Optional[Dict[str, Any]] = None
