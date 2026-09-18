"""Schema definitions for YouTube endpoints."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class YouTubeVideoRequest(BaseModel):
    """Input for a single video extraction request."""

    video_url: str = Field(..., description="YouTube video URL or video id")
    include_comments: bool = Field(default=False)
    include_transcript: bool = Field(default=False)


class YouTubeChannelRequest(BaseModel):
    """Input for a channel extraction request."""

    channel_url: str = Field(..., description="YouTube channel URL")
    max_videos: int = Field(default=20, ge=1, le=100)
    include_comments: bool = Field(default=False)


class YouTubeVideoResponse(BaseModel):
    """Response model for scraped video metadata."""

    video_id: str
    title: str
    channel: Optional[str] = None
    channel_id: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    published_at: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    thumbnail_url: Optional[str] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class YouTubeChannelResponse(BaseModel):
    """Channel extraction response."""

    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    videos: List[YouTubeVideoResponse] = Field(default_factory=list)
    total_videos: int = 0
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class YouTubeBatchRequest(BaseModel):
    """Batch extraction request."""

    video_urls: List[str] = Field(..., min_length=1)
    include_comments: bool = Field(default=False)


class YouTubeBatchResponse(BaseModel):
    """Batch extraction response."""

    videos: List[YouTubeVideoResponse] = Field(default_factory=list)
    total: int = 0
