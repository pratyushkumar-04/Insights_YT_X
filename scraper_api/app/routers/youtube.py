"""YouTube router."""

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_optional_api_key
from app.schemas.youtube import (
    YouTubeBatchRequest,
    YouTubeBatchResponse,
    YouTubeChannelRequest,
    YouTubeChannelResponse,
    YouTubeVideoRequest,
    YouTubeVideoResponse,
)
from app.services.youtube_service import youtube_service

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.get("/health")
async def youtube_health() -> dict:
    """Health endpoint for the YouTube scraper."""
    return {"status": "ok", "service": "youtube"}


@router.post("/video", response_model=YouTubeVideoResponse, dependencies=[Depends(get_optional_api_key)])
async def extract_video(request: YouTubeVideoRequest) -> YouTubeVideoResponse:
    """Extract a single YouTube video's metadata."""
    payload = await youtube_service.extract_video(
        video_url=request.video_url,
        include_comments=request.include_comments,
        include_transcript=request.include_transcript,
    )
    return YouTubeVideoResponse(**payload)


@router.post("/channel", response_model=YouTubeChannelResponse, dependencies=[Depends(get_optional_api_key)])
async def extract_channel(request: YouTubeChannelRequest) -> YouTubeChannelResponse:
    """Extract metadata for videos in a YouTube channel."""
    payload = await youtube_service.extract_channel(
        channel_url=request.channel_url,
        max_videos=request.max_videos,
        include_comments=request.include_comments,
    )
    return YouTubeChannelResponse(**payload)


@router.post("/batch", response_model=YouTubeBatchResponse, dependencies=[Depends(get_optional_api_key)])
async def extract_batch(request: YouTubeBatchRequest) -> YouTubeBatchResponse:
    """Extract several YouTube videos in one request."""
    payload = await youtube_service.extract_batch(
        video_urls=request.video_urls,
        include_comments=request.include_comments,
    )
    return YouTubeBatchResponse(**payload)
