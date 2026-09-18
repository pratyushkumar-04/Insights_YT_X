"""Service layer for Telegram scraping operations."""

from __future__ import annotations

import os
from typing import Any, Dict

from app.core.logging import get_logger
from app.exceptions import ScraperUpstreamError, ScraperValidationError

logger = get_logger(__name__)


class TelegramService:
    """Thin wrapper around Telegram scraping logic."""

    async def get_channel_messages(self, channel_name: str, limit: int = 20) -> Dict[str, Any]:
        """Fetch channel messages from a Telegram source."""
        try:
            if not channel_name or not channel_name.strip():
                raise ScraperValidationError("Telegram channel name is required.")

            api_id = os.getenv("TELEGRAM_API_ID")
            api_hash = os.getenv("TELEGRAM_API_HASH")
            if not api_id or not api_hash:
                raise ScraperValidationError(
                    "Telegram API credentials are missing. Set TELEGRAM_API_ID and TELEGRAM_API_HASH in the environment."
                )

            from telethon import TelegramClient

            async with TelegramClient("telegram_session_api", int(api_id), api_hash) as client:
                entity = await client.get_entity(channel_name.strip())
                messages = []
                async for message in client.iter_messages(entity, limit=limit):
                    messages.append(
                        {
                            "message_id": str(getattr(message, "id", None)),
                            "text": getattr(message, "text", None),
                            "sender": getattr(getattr(message, "sender", None), "username", None),
                            "channel": getattr(entity, "username", None) or getattr(entity, "title", None),
                            "date": getattr(message, "date", None).isoformat() if getattr(message, "date", None) else None,
                            "raw_data": {
                                "id": getattr(message, "id", None),
                                "date": getattr(message, "date", None).isoformat() if getattr(message, "date", None) else None,
                                "views": getattr(message, "views", None),
                                "forwards": getattr(message, "forwards", None),
                            },
                        }
                    )

            logger.info("telegram_channel_request", channel_name=channel_name, limit=limit, total=len(messages))
            return {"channel_name": channel_name, "messages": messages, "total": len(messages), "raw_data": {"count": len(messages)}}
        except ScraperValidationError:
            raise
        except Exception as exc:
            logger.exception("telegram_channel_failed", exc_info=exc)
            raise ScraperUpstreamError("Failed to fetch Telegram channel messages") from exc


telegram_service = TelegramService()
