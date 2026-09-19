"""Schema definitions for Twitter/X endpoints."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TwitterSearchRequest(BaseModel):
    """Input for a tweet search on Twitter/X."""

    query: str = Field(..., min_length=1)
    max_results: int = Field(default=20, ge=1, le=100)
    language: Optional[str] = None
    since: Optional[str] = None
    until: Optional[str] = None


class TwitterUserRequest(BaseModel):
    """Input for a Twitter user profile lookup."""

    username: str = Field(..., min_length=1)
    include_posts: bool = Field(default=False)
    max_posts: int = Field(default=10, ge=1, le=50)


class TwitterTweetRequest(BaseModel):
    """Input for scraping a single tweet."""

    tweet_id: str = Field(..., min_length=1)


class TwitterPost(BaseModel):
    id: str
    text: str
    author: str | None
    author_id: str | None
    created_at: str | None
    likes: int
    retweets: int
    replies: int
    comments: list[dict] = Field(default_factory=list)
    raw_data: dict = Field(default_factory=dict)
    saved_file: Optional[str] = None


class TwitterSearchResponse(BaseModel):
    """Response for a search on Twitter/X."""

    query: str
    results: List[TwitterPost] = Field(default_factory=list)
    total: int = 0
    saved_file: Optional[str] = None


class TwitterUserResponse(BaseModel):
    """Payload for a Twitter user profile response."""

    username: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    verified: Optional[bool] = False
    posts: List[TwitterPost] = Field(default_factory=list)
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    saved_file: Optional[str] = None
