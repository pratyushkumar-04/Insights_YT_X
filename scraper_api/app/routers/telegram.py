"""Telegram router."""

from fastapi import APIRouter, Depends

from app.dependencies import get_optional_api_key
from app.schemas.telegram import TelegramChannelRequest, TelegramChannelResponse
from app.services.telegram_service import telegram_service

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.get("/health")
async def telegram_health() -> dict:
    """Health endpoint for the Telegram scraper."""
    return {"status": "ok", "service": "telegram"}


@router.post("/channel", response_model=TelegramChannelResponse, dependencies=[Depends(get_optional_api_key)])
async def get_messages(request: TelegramChannelRequest) -> TelegramChannelResponse:
    """Fetch messages from a Telegram channel."""
    payload = await telegram_service.get_channel_messages(
        channel_name=request.channel_name,
        limit=request.limit,
    )
    return TelegramChannelResponse(**payload)
