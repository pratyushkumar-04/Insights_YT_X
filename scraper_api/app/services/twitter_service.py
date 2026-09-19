"""Service layer for Twitter/X scraping operations."""

from __future__ import annotations

import asyncio
import json
import os
import socket
import ssl
import sys
from datetime import datetime, timezone
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


def _get_twitter_data_dir() -> Path:
    return (ROOT_DIR / "data" / "Twitter").resolve()


def _safe_json_dump(data: Any, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, default=str)


def _save_twitter_payload(prefix: str, payload: Dict[str, Any]) -> str:
    twitter_dir = _get_twitter_data_dir()
    twitter_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = twitter_dir / f"{prefix}_{timestamp}.json"
    _safe_json_dump(payload, file_path)
    return str(file_path)


def _diagnose_network() -> Dict[str, Any]:
    env_names = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy"]
    proxy_state = {}
    for name in env_names:
        value = os.getenv(name)
        if value:
            proxy_state[name] = "set"
        else:
            proxy_state[name] = "unset"

    results = {
        "proxy_variables": proxy_state,
        "python_dns_x_com": False,
        "python_dns_abs_twitter": False,
        "python_https_x_com": False,
    }

    for host in ("x.com", "abs.twimg.com"):
        try:
            socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
            results[f"python_dns_{host.replace('.', '_')}"] = True
        except Exception:
            results[f"python_dns_{host.replace('.', '_')}"] = False

    try:
        context = ssl.create_default_context()
        with socket.create_connection(("x.com", 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname="x.com") as ssock:
                results["python_https_x_com"] = True
                results["python_https_x_com_server"] = ssock.version()
    except Exception as exc:
        results["python_https_x_com"] = False
        results["python_https_x_com_error"] = str(exc)

    return results


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
            logger.info("twitter_network_diagnostics", diagnostics=_diagnose_network())

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

            payload = {
                "query": query,
                "results": formatted_results,
                "total": len(formatted_results),
                "saved_at": datetime.now(timezone.utc).isoformat(),
            }
            saved_file = _save_twitter_payload("search", payload)

            return {
                "query": query,
                "results": [],
                "total": len(formatted_results),
                "saved_file": saved_file,
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

            payload = {
                "username": profile.get("username") or username_clean,
                "display_name": profile.get("display_name"),
                "bio": profile.get("bio"),
                "followers": profile.get("followers"),
                "following": profile.get("following"),
                "verified": bool(profile.get("verified")),
                "posts": posts,
                "raw_data": profile,
                "saved_at": datetime.now(timezone.utc).isoformat(),
            }
            saved_file = _save_twitter_payload(f"user_{username_clean}", payload)

            return {
                "username": profile.get("username") or username_clean,
                "display_name": profile.get("display_name"),
                "bio": profile.get("bio"),
                "followers": profile.get("followers"),
                "following": profile.get("following"),
                "verified": bool(profile.get("verified")),
                "posts": [],
                "raw_data": {},
                "saved_file": saved_file,
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

            payload = self._format_post(
                tweet,
                tweet.get("author_username") or "",
            )
            payload["saved_at"] = datetime.now(timezone.utc).isoformat()
            saved_file = _save_twitter_payload(f"tweet_{tweet.get('id') or tweet.get('tweet_id') or 'single'}", {"result": payload})
            payload["saved_file"] = saved_file
            return payload

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
