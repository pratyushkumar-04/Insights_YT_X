"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.core.logging import get_logger, setup_logging
from app.core.rate_limiter import limiter
from app.exceptions import (
    ScraperAPIException,
    generic_exception_handler,
    http_exception_handler,
    scraper_api_exception_handler,
    validation_exception_handler,
)
from app.middleware import register_middleware
from app.routers.health import router as health_router
from app.routers.telegram import router as telegram_router
from app.routers.twitter import router as twitter_router
from app.routers.youtube import router as youtube_router

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Production-ready API wrapper for YouTube, Twitter/X, and Telegram scraping workflows.",
)

register_middleware(app)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(ScraperAPIException, scraper_api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, lambda request, exc: http_exception_handler(request, exc))
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(ValueError, generic_exception_handler)

app.include_router(health_router)
app.include_router(youtube_router)
app.include_router(twitter_router)
app.include_router(telegram_router)


@app.get("/")
async def root() -> dict:
    """Root endpoint providing service metadata."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ok",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
