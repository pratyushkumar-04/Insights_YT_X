"""Service layer for Telegram scraping operations."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from app.core.logging import get_logger
from app.exceptions import ScraperUpstreamError, ScraperValidationError

logger = get_logger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[3]
TELEGRAM_SESSION_FILE = ROOT_DIR / "telegram_session.session"
CONNECT_TIMEOUT_SECONDS = 15
REQUEST_TIMEOUT_SECONDS = 30

# Credentials and the existing authorized session live in different places.
# Load credentials independently of the directory from which Uvicorn starts.
load_dotenv(ROOT_DIR / "scraper_api" / ".env")


class TelegramService:
    """Fetch Telegram data with the existing, non-interactive session."""

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

            if not TELEGRAM_SESSION_FILE.is_file():
                raise ScraperUpstreamError(
                    f"Telegram session file was not found: {TELEGRAM_SESSION_FILE}. "
                    "Create an authorized telegram_session.session before starting the API."
                )

            from telethon import TelegramClient

            # Do not use client.start() or an async client context manager here:
            # either can start Telethon's interactive phone/OTP login flow.
            # connect() only opens the saved session, while is_user_authorized()
            # lets the API return a useful error if it has expired.
            client = TelegramClient(
                str(TELEGRAM_SESSION_FILE),
                int(api_id),
                api_hash,
                timeout=CONNECT_TIMEOUT_SECONDS,
                request_retries=1,
                connection_retries=1,
                retry_delay=1,
                auto_reconnect=False,
            )
            logger.info(
                "telegram_session_connecting",
                session_file=TELEGRAM_SESSION_FILE.name,
                timeout_seconds=CONNECT_TIMEOUT_SECONDS,
            )
            await asyncio.wait_for(client.connect(), timeout=CONNECT_TIMEOUT_SECONDS)
            try:
                logger.info("telegram_session_connected")
                logger.info("telegram_session_authorizing")
                authorized = await asyncio.wait_for(
                    client.is_user_authorized(), timeout=REQUEST_TIMEOUT_SECONDS
                )
                if not authorized:
                    raise ScraperUpstreamError(
                        "The saved Telegram session is not authorized or has expired. "
                        "Re-create telegram_session.session outside the API; this endpoint never prompts for a phone number or OTP."
                    )

                logger.info("telegram_session_authorized")
                logger.info("telegram_channel_resolving", channel_name=channel_name)
                entity = await asyncio.wait_for(
                    client.get_entity(channel_name.strip()), timeout=REQUEST_TIMEOUT_SECONDS
                )
                logger.info(
                    "telegram_messages_fetching",
                    channel=getattr(entity, "username", None) or getattr(entity, "title", None),
                    limit=limit,
                )
                # get_messages is a single bounded RPC.  iter_messages can
                # keep awaiting subsequent pages indefinitely after a network
                # failure, which was leaving this endpoint open forever.
                fetched_messages = await asyncio.wait_for(
                    client.get_messages(entity, limit=limit), timeout=REQUEST_TIMEOUT_SECONDS
                )
                messages = []
                for message in fetched_messages:
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
            finally:
                logger.info("telegram_session_disconnecting")
                try:
                    await asyncio.wait_for(client.disconnect(), timeout=5)
                except Exception as disconnect_error:  # cleanup must not hide the request result
                    logger.warning("telegram_session_disconnect_failed", error=str(disconnect_error))

            logger.info("telegram_channel_request", channel_name=channel_name, limit=limit, total=len(messages))
            return {"channel_name": channel_name, "messages": messages, "total": len(messages), "raw_data": {"count": len(messages)}}
        except (ScraperValidationError, ScraperUpstreamError):
            raise
        except asyncio.TimeoutError as exc:
            logger.error(
                "telegram_channel_timeout",
                channel_name=channel_name,
                connect_timeout_seconds=CONNECT_TIMEOUT_SECONDS,
                request_timeout_seconds=REQUEST_TIMEOUT_SECONDS,
            )
            raise ScraperUpstreamError(
                "Telegram did not respond in time. Check the network/channel and try again."
            ) from exc
        except Exception as exc:
            logger.exception("telegram_channel_failed", exc_info=exc)
            raise ScraperUpstreamError("Failed to fetch Telegram channel messages") from exc


telegram_service = TelegramService()
