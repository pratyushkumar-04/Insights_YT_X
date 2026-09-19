"""Application configuration using Pydantic Settings."""

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Scraper API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    API_KEY_HEADER: str = "X-API-Key"
    API_KEYS: List[str] = []
    REQUIRE_API_KEY: bool = False

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "60/minute"

    SCRAPER_TIMEOUT: int = 300
    SCRAPER_MAX_RETRIES: int = 3

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    METRICS_ENABLED: bool = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def normalize_debug_value(cls, value: object) -> object:
        """Accept deployment labels accidentally supplied as DEBUG values."""
        if isinstance(value, str) and value.strip().lower() in {"release", "production", "prod"}:
            return False
        return value


settings = Settings()
