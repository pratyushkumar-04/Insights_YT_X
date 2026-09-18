"""Shared FastAPI dependencies."""

from typing import Optional

from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader

from app.config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)


async def get_api_key(api_key: Optional[str] = Security(api_key_header)) -> Optional[str]:
    """Validate API keys when enabled."""
    if not settings.REQUIRE_API_KEY:
        return None

    if not api_key or api_key not in settings.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key


async def get_request_context(request: Request) -> Request:
    """Attach a request id and context to the request."""
    if not hasattr(request.state, "request_id"):
        request.state.request_id = request.headers.get("X-Request-ID", "unknown")
    return request


async def get_optional_api_key(
    request: Request,
    api_key: Optional[str] = Depends(get_api_key),
) -> Optional[str]:
    """Dependency for endpoints that optionally accept API keys."""
    return api_key
