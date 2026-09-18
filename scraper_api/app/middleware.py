"""HTTP middleware for request tracking and CORS."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach request metadata to each request before it reaches handlers."""

    async def dispatch(self, request, call_next):
        request.state.request_id = request.headers.get("X-Request-ID", "unknown")
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(request.state.request_id)
        return response


def register_middleware(app: FastAPI) -> None:
    """Register common middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    app.add_middleware(RequestContextMiddleware)
