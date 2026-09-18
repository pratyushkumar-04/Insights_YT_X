"""Twitter/X router."""

from fastapi import APIRouter, Depends

from app.dependencies import get_optional_api_key
from app.schemas.twitter import (
    TwitterSearchRequest,
    TwitterSearchResponse,
    TwitterTweetRequest,
    TwitterUserRequest,
    TwitterUserResponse,
    TwitterPost,
)
from app.services.twitter_service import twitter_service

router = APIRouter(prefix="/twitter", tags=["twitter"])


@router.get("/health")
async def twitter_health() -> dict:
    """Health endpoint for the Twitter scraper."""
    return {"status": "ok", "service": "twitter"}


@router.post("/search", response_model=TwitterSearchResponse, dependencies=[Depends(get_optional_api_key)])
async def search_tweets(request: TwitterSearchRequest) -> TwitterSearchResponse:
    """Search Twitter/X posts."""
    payload = await twitter_service.search_tweets(
        query=request.query,
        max_results=request.max_results,
        language=request.language,
        since=request.since,
        until=request.until,
    )
    return TwitterSearchResponse(**payload)


@router.post("/user", response_model=TwitterUserResponse, dependencies=[Depends(get_optional_api_key)])
async def fetch_user(request: TwitterUserRequest) -> TwitterUserResponse:
    """Fetch Twitter/X user metadata and optional posts."""
    payload = await twitter_service.get_user_profile(
        username=request.username,
        include_posts=request.include_posts,
        max_posts=request.max_posts,
    )
    return TwitterUserResponse(**payload)


@router.post("/tweet", response_model=TwitterPost, dependencies=[Depends(get_optional_api_key)])
async def fetch_tweet(request: TwitterTweetRequest) -> TwitterPost:
    """Fetch a single tweet by id."""
    payload = await twitter_service.get_tweet_by_id(request.tweet_id)
    return TwitterPost(**payload)
