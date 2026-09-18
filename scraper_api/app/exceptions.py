"""Custom exceptions and handlers for the scraper API."""

from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)


class ScraperAPIException(Exception):
    """Base API exception."""

    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ScraperNotFoundError(ScraperAPIException):
    """Raised when a requested resource cannot be found."""

    def __init__(self, resource: str):
        super().__init__(message=f"Resource not found: {resource}", status_code=404)


class ScraperValidationError(ScraperAPIException):
    """Raised when request inputs are invalid."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)


class ScraperRateLimitError(ScraperAPIException):
    """Raised when rate limits are exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, status_code=429)


class ScraperAuthError(ScraperAPIException):
    """Raised when auth fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=401)


class ScraperUpstreamError(ScraperAPIException):
    """Raised when the upstream scraper fails."""

    def __init__(self, message: str = "Upstream service error"):
        super().__init__(message=message, status_code=502)


async def scraper_api_exception_handler(request: Request, exc: ScraperAPIException):
    """Handle custom scraper API exceptions."""
    logger.error(
        "api_exception",
        path=request.url.path,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": exc.message,
            "details": exc.details,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning("validation_error", path=request.url.path, errors=exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": "Validation error",
            "details": exc.errors(),
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        },
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.warning(
        "http_exception",
        path=request.url.path,
        status_code=exc.status_code,
        detail=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": exc.detail,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions."""
    logger.exception("unhandled_exception", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": "Internal server error",
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        },
    )
