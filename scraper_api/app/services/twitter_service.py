"""Service layer for Twitter/X scraping operations."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()

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

    def __init__(self) -> None:
        self._scraper: TwitterScraper | None = None

    def _build_scraper(self) -> TwitterScraper:
        if self._scraper is not None:
            return self._scraper

        token = os.getenv("TWITTER_AUTH_TOKEN")

        logger.info(
            "twitter_token_loaded",
            exists=bool(token),
            length=len(token) if token else 0,
        )

        self._scraper = TwitterScraper(auth_token=token)
        return self._scraper

    @staticmethod
    def _format_account_error(exc: Exception) -> str:
        msg = str(exc)

        if (
            "No eligible accounts" in msg
            or "AccountPoolExhausted" in msg
            or "Check your credentials" in msg
        ):
            return (
                "Twitter/X authentication or account availability failed. "
                "Check the TWITTER_AUTH_TOKEN and ensure the Scweet account pool is active."
            )

        return "Failed to search Twitter/X posts"

    @staticmethod
    def _format_post(post: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Convert a Scweet post into the API's TwitterPost format."""

        return {
            "id": post.get("tweet_id"),
            "text": post.get("text") or "",
            "author": post.get("author_username") or username,
            "author_id": post.get("author_id"),
            "created_at": post.get("timestamp"),
            "likes": post.get("likes") or 0,
            "retweets": post.get("retweets") or 0,
            "replies": post.get("replies") or 0,

            # Actual reply/comment objects
            "comments": post.get("comments") or post.get("replies_data") or [],

            "raw_data": post,
        }

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
                raise ScraperValidationError(
                    "Query text is required for Twitter search."
                )

            scraper = self._build_scraper()

            results = await asyncio.to_thread(
                scraper.search_tweets,
                query.strip(),
                since,
                until,
                max_results,
            )

            formatted_results = [
                self._format_post(post, "")
                for post in results
            ]

            logger.info(
                "twitter_search_request",
                query=query,
                max_results=max_results,
            )

            return {
                "query": query,
                "results": formatted_results,
                "total": len(formatted_results),
            }

        except ScraperValidationError:
            raise

        except (AccountPoolExhausted, LookupError) as exc:
            logger.exception("twitter_search_failed", exc_info=exc)
            raise ScraperUpstreamError(
                self._format_account_error(exc)
            ) from exc

        except Exception as exc:
            logger.exception("twitter_search_failed", exc_info=exc)
            raise ScraperUpstreamError(
                self._format_account_error(exc)
            ) from exc

    async def get_user_profile(
        self,
        username: str,
        include_posts: bool = False,
        max_posts: int = 10,
    ) -> Dict[str, Any]:
        """Fetch Twitter/X user profile and optional recent posts."""

        try:
            if not username or not username.strip():
                raise ScraperValidationError(
                    "Twitter username is required."
                )

            scraper = self._build_scraper()

            username_clean = username.strip().lstrip("@")

            profile = await asyncio.to_thread(
                scraper.get_profile,
                username_clean,
            )

            posts = []

            if include_posts:
                raw_posts = await asyncio.to_thread(
                    scraper.get_user_posts,
                    username_clean,
                    max_posts,
                    True,
                    100,
                )

                posts = [
                    self._format_post(post, username_clean)
                    for post in raw_posts
                ]

            logger.info(
                "twitter_profile_request",
                username=username,
                include_posts=include_posts,
            )

            return {
                "username": profile.get("username") or username_clean,
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
            raise ScraperUpstreamError(
                self._format_account_error(exc)
            ) from exc

        except Exception as exc:
            logger.exception("twitter_profile_failed", exc_info=exc)
            raise ScraperUpstreamError(
                self._format_account_error(exc)
            ) from exc

    async def get_tweet_by_id(
        self,
        tweet_id: str,
    ) -> Dict[str, Any]:
        """Fetch a single tweet by ID."""

        try:
            if not tweet_id or not tweet_id.strip():
                raise ScraperValidationError(
                    "Tweet ID or URL is required."
                )

            scraper = self._build_scraper()

            tweet = await asyncio.to_thread(
                scraper.extract_post,
                tweet_id.strip(),
                fetch_replies=True,
            )

            logger.info(
                "twitter_tweet_request",
                tweet_id=tweet_id,
            )

            return self._format_post(
                tweet,
                tweet.get("author_username") or "",
            )

        except ScraperValidationError:
            raise

        except (AccountPoolExhausted, LookupError) as exc:
            logger.exception("twitter_tweet_failed", exc_info=exc)
            raise ScraperUpstreamError(
                self._format_account_error(exc)
            ) from exc

        except Exception as exc:
            logger.exception("twitter_tweet_failed", exc_info=exc)
            raise ScraperUpstreamError(
                self._format_account_error(exc)
            ) from exc


twitter_service = TwitterService()
