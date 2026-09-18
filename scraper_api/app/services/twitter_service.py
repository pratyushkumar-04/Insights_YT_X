"""Service layer for Twitter/X scraping operations."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict

from app.core.logging import get_logger
from app.exceptions import ScraperUpstreamError, ScraperValidationError

try:
    from Scweet.exceptions import AccountPoolExhausted
except ImportError:  # pragma: no cover - optional dependency may not be installed
    class AccountPoolExhausted(Exception):
        pass

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.twitter_scraper import TwitterScraper

logger = get_logger(__name__)


class TwitterService:
    """Thin wrapper around the existing Twitter/X scraper logic."""

    @staticmethod
    def _build_scraper() -> TwitterScraper:
        return TwitterScraper(auth_token=os.getenv("TWITTER_AUTH_TOKEN"))

    @staticmethod
    def _format_account_error(exc: Exception) -> str:
        msg = str(exc)
        if "No eligible accounts" in msg or "AccountPoolExhausted" in msg or "Check your credentials" in msg:
            return (
                "Twitter/X authentication or account availability failed. "
                "Check the TWITTER_AUTH_TOKEN and ensure the Scweet account pool is active."
            )
        return "Failed to search Twitter/X posts"

    async def search_tweets(
        self,
        query: str,
        max_results: int = 20,
        language: str | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> Dict[str, Any]:
        """Search Twitter/X for posts matching the query."""
        try:
            if not query or not query.strip():
                raise ScraperValidationError("Query text is required for Twitter search.")

            scraper = self._build_scraper()
            results = await asyncio.to_thread(
                scraper.search_tweets,
                query.strip(),
                since,
                until,
                max_results,
            )
            logger.info("twitter_search_request", query=query, max_results=max_results)
            return {"query": query, "results": results, "total": len(results)}
        except ScraperValidationError:
            raise
        except (AccountPoolExhausted, LookupError) as exc:
            logger.exception("twitter_search_failed", exc_info=exc)
            raise ScraperUpstreamError(self._format_account_error(exc)) from exc
        except Exception as exc:
            logger.exception("twitter_search_failed", exc_info=exc)
            raise ScraperUpstreamError(self._format_account_error(exc)) from exc

    async def get_user_profile(self, username: str, include_posts: bool = False, max_posts: int = 10) -> Dict[str, Any]:
        """Fetch a Twitter/X profile."""
        try:
            if not username or not username.strip():
                raise ScraperValidationError("Twitter username is required.")

            scraper = self._build_scraper()
            username_clean = username.strip().lstrip("@")
            profile = await asyncio.to_thread(scraper.get_profile, username_clean)
            posts = []
            if include_posts:
                posts = await asyncio.to_thread(scraper.get_user_posts, username_clean, max_posts)
            logger.info("twitter_profile_request", username=username, include_posts=include_posts)
            return {
                "username": profile.get("username") or username.strip().lstrip("@"),
                "display_name": profile.get("display_name"),
                "bio": profile.get("bio"),
                "followers": profile.get("followers"),
                "following": profile.get("following"),
                "verified": bool(profile.get("verified")),
                "posts": posts,
                "raw_data": profile,
            }
        except ScraperValidationError:
            raise
        except (AccountPoolExhausted, LookupError) as exc:
            logger.exception("twitter_profile_failed", exc_info=exc)
            raise ScraperUpstreamError(self._format_account_error(exc)) from exc
        except Exception as exc:
            logger.exception("twitter_profile_failed", exc_info=exc)
            raise ScraperUpstreamError(self._format_account_error(exc)) from exc

    async def get_tweet_by_id(self, tweet_id: str) -> Dict[str, Any]:
        """Fetch a single tweet by ID."""
        try:
            if not tweet_id or not tweet_id.strip():
                raise ScraperValidationError("Tweet ID or URL is required.")

            scraper = self._build_scraper()
            tweet = await asyncio.to_thread(scraper.extract_post, tweet_id.strip())
            logger.info("twitter_tweet_request", tweet_id=tweet_id)
            return {
                "id": tweet.get("tweet_id") or tweet_id.strip(),
                "text": tweet.get("text") or "",
                "author": tweet.get("author_username") or None,
                "author_id": None,
                "created_at": tweet.get("timestamp") or None,
                "likes": tweet.get("likes") or 0,
                "retweets": tweet.get("retweets") or 0,
                "replies": tweet.get("replies") or 0,
                "raw_data": tweet,
            }
        except ScraperValidationError:
            raise
        except (AccountPoolExhausted, LookupError) as exc:
            logger.exception("twitter_tweet_failed", exc_info=exc)
            raise ScraperUpstreamError(self._format_account_error(exc)) from exc
        except Exception as exc:
            logger.exception("twitter_tweet_failed", exc_info=exc)
            raise ScraperUpstreamError(self._format_account_error(exc)) from exc


twitter_service = TwitterService()
