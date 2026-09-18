"""Schema definitions for Telegram endpoints."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TelegramChannelRequest(BaseModel):
    """Input for Telegram channel extraction."""

    channel_name: str = Field(..., min_length=1)
    limit: int = Field(default=20, ge=1, le=100)


class TelegramMessage(BaseModel):
    """Normalized Telegram message."""

    message_id: Optional[str] = None
    text: Optional[str] = None
    sender: Optional[str] = None
    channel: Optional[str] = None
    date: Optional[str] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class TelegramChannelResponse(BaseModel):
    """Telegram channel extraction response."""

    channel_name: str
    messages: List[TelegramMessage] = Field(default_factory=list)
    total: int = 0
    raw_data: Dict[str, Any] = Field(default_factory=dict)
