"""Twitter/X scraping, normalization, persistence, and summary helpers.

Scweet is deliberately imported lazily so URL parsing and export tests can run
without a browser, cookies, or an authenticated X account.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence
from urllib.parse import urlparse

import pandas as pd


@dataclass
class TwitterConfig:
    default_directory: str = "data/twitter"
    rate_limit_seconds: float = 2.5
    # One initial call plus at most three retries.
    retry_attempts: int = 3
    retry_backoff_seconds: float = 2.0
    logging_level: str = "INFO"
    output_formats: List[str] = field(default_factory=lambda: ["json", "csv", "excel"])
    headless: bool = True
    max_reply_depth: int = 3

    @classmethod
    def from_file(cls, path: str | Path) -> "TwitterConfig":
        with open(path, "r", encoding="utf-8") as stream:
            values = json.load(stream)
        return cls(**{key: value for key, value in values.items() if key in cls.__dataclass_fields__})


def _logger(config: TwitterConfig) -> logging.Logger:
    logger = logging.getLogger("twitter_scraper")
    logger.setLevel(getattr(logging, config.logging_level.upper(), logging.INFO))
    log_dir = Path(config.default_directory).resolve()
    if getattr(logger, "_twitter_log_directory", None) != log_dir:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        log_dir.mkdir(parents=True, exist_ok=True)
        for filename in ("twitter_scraper.log", "twitter_scraper_debug.log"):
            handler = logging.FileHandler(log_dir / filename, encoding="utf-8")
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG if "debug" in filename else logger.level)
            logger.addHandler(handler)
        logger._twitter_log_directory = log_dir
    return logger


class TwitterScraper:
    """High-level Twitter/X scraper backed by Scweet."""

    TWEET_ID = re.compile(r"/status/(\d{5,25})(?:[/?#]|$)")
    USERNAME = re.compile(r"^[A-Za-z0-9_]{1,15}$")

    def __init__(
        self,
        auth_token: Optional[str] = None,
        config: Optional[TwitterConfig] = None,
        client: Any = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config or TwitterConfig()
        self.auth_token = auth_token
        self._client = client
        self._sleep = sleep
        self._last_request = 0.0
        # A scraper is shared by the API service.  Serialising client calls
        # keeps its request interval effective when FastAPI handles requests
        # concurrently.
        self._request_lock = threading.Lock()
        self.logger = _logger(self.config)

    @staticmethod
    def extract_tweet_id(url_or_id: str) -> Optional[str]:
        value = str(url_or_id).strip()
        if value.isdigit() and 5 <= len(value) <= 25:
            return value
        parsed = urlparse(value if "://" in value else f"https://x.com/{value}")
        if parsed.netloc.lower() not in {"twitter.com", "www.twitter.com", "x.com", "www.x.com"}:
            return None
        match = TwitterScraper.TWEET_ID.search(parsed.path)
        return match.group(1) if match else None

    def _build_client(self) -> Any:
        if self._client is None:
            try:
                from Scweet import Scweet, ScweetConfig
            except ImportError as error:
                raise RuntimeError("Scweet is required. Install dependencies with: pip install -r requirements.txt") from error
            
            kwargs: Dict[str, Any] = {
                "config": ScweetConfig(daily_requests_limit=10000, daily_tweets_limit=100000)
            }
            if self.auth_token:
                kwargs["auth_token"] = self.auth_token
            self._client = Scweet(**kwargs)
        return self._client

    def close(self) -> None:
        """Release scraper-owned log handlers, useful for long-running processes and tests."""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
        self.logger._twitter_log_directory = None

    def _call(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        client = self._build_client()
        method = getattr(client, method_name, None)
        if method is None:
            raise RuntimeError(f"The installed Scweet client does not support {method_name}()")
        with self._request_lock:
            elapsed = time.monotonic() - self._last_request
            if elapsed < self.config.rate_limit_seconds:
                self._sleep(self.config.rate_limit_seconds - elapsed)
            for attempt in range(self.config.retry_attempts + 1):
                started = time.perf_counter()
                try:
                    self.logger.debug("Scweet request method=%s args=%s kwargs=%s", method_name, args, kwargs)
                    result = method(*args, **kwargs)
                    self._last_request = time.monotonic()
                    self.logger.info("Scweet request method=%s completed in %.2fs", method_name, time.perf_counter() - started)
                    return result
                except Exception as error:
                    self._last_request = time.monotonic()
                    if attempt >= self.config.retry_attempts:
                        self.logger.exception("Scweet request failed after %d retries", attempt)
                        raise
                    delay = self.config.retry_backoff_seconds * (2 ** attempt)
                    self.logger.warning("Scweet request failed (%s); retrying in %.1fs", error, delay)
                    self._sleep(delay)

    @staticmethod
    def _rows(value: Any) -> List[Dict[str, Any]]:
        if value is None:
            return []
        if isinstance(value, pd.DataFrame):
            return value.to_dict(orient="records")
        if isinstance(value, Mapping):
            return [dict(value)]
        return [dict(row) if isinstance(row, Mapping) else {"value": row} for row in value]

    @staticmethod
    def _first(row: Mapping[str, Any], *names: str, default: Any = None) -> Any:
        for name in names:
            if name in row and row[name] not in (None, ""):
                return row[name]
        return default

    @classmethod
    def normalize_tweet(cls, row: Mapping[str, Any]) -> Dict[str, Any]:
        text = str(cls._first(row, "text", "tweet_text", "content", default=""))
        tweet_id = str(cls._first(row, "tweet_id", "id", "id_str", default=""))
        user = row.get("user") if isinstance(row.get("user"), Mapping) else {}
        media = row.get("media") if isinstance(row.get("media"), Mapping) else {}
        hashtags = re.findall(r"(?<!\w)#([\w]+)", text)
        mentions = re.findall(r"(?<!\w)@([A-Za-z0-9_]+)", text)
        timestamp = cls._first(row, "timestamp", "date", "created_at", "time")
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        return {
            "tweet_id": tweet_id,
            "text": text,
            "author_username": cls._first(row, "author_username", "user_screen_name", "username", "user_name", default=user.get("screen_name")),
            "author_display_name": cls._first(row, "author_display_name", "display_name", "user_name", default=user.get("name")),
            "timestamp": timestamp,
            "likes": cls._first(row, "likes", "like_count", "favorite_count", default=0),
            "retweets": cls._first(row, "retweets", "retweet_count", default=0),
            "replies": cls._first(row, "replies", "comments", "reply_count", "conversation_count", default=0),
            "views": cls._first(row, "views", "view_count", default=0),
            "hashtags": list(dict.fromkeys(hashtags)),
            "mentions": list(dict.fromkeys(mentions)),
            "image_urls": cls._first(row, "image_urls", "photos", "images", default=media.get("image_links", [])),
            "video_urls": cls._first(row, "video_urls", "videos", default=media.get("video_links", [])),
            "source": cls._first(row, "source", "client", default=None),
            "is_retweet": bool(cls._first(row, "is_retweet", "retweet", default=False)) or text.startswith("RT @"),
            "quote_tweet": cls._first(row, "quote_tweet", "quoted_tweet", "embedded_text", default=None),
            "in_reply_to_id": cls._first(row, "in_reply_to_id", "in_reply_to_status_id", "conversation_id"),
            "url": cls._first(row, "url", "tweet_url", default=f"https://x.com/i/status/{tweet_id}" if tweet_id else None),
        }

    def extract_post(self, url_or_id: str, fetch_replies: bool = False, max_replies: int = 50) -> Dict[str, Any]:
        tweet_id = self.extract_tweet_id(url_or_id)
        if not tweet_id:
            raise ValueError("Expected a valid Twitter/X status URL or numeric tweet ID")
        
        author_username = None
        parsed = urlparse(url_or_id if "://" in url_or_id else f"https://x.com/{url_or_id}")
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 3 and parts[1] == "status":
            author_username = parts[0]
        
        target_tweet = None
        if author_username and self.USERNAME.fullmatch(author_username):
            try:
                user_tweets = self.search_tweets(f"from:{author_username}", count=50)
                for tweet in user_tweets:
                    if tweet.get("tweet_id") == tweet_id:
                        target_tweet = tweet
                        break
            except Exception as err:
                self.logger.warning("Search from:%s failed: %s", author_username, err)
        
        if not target_tweet:
            rows = self._rows(self._call("search", f"conversation_id:{tweet_id}", limit=20, save=False))
            matches = [self.normalize_tweet(row) for row in rows if str(self._first(row, "tweet_id", "id", "id_str", default="")) == tweet_id]
            if matches:
                target_tweet = matches[0]
            else:
                rows_direct = self._rows(self._call("search", tweet_id, limit=20, save=False))
                matches_direct = [self.normalize_tweet(row) for row in rows_direct if str(self._first(row, "tweet_id", "id", "id_str", default="")) == tweet_id]
                if matches_direct:
                    target_tweet = matches_direct[0]
                elif rows:
                    for row in rows:
                        norm = self.normalize_tweet(row)
                        parent_user = norm.get("author_username")
                        if parent_user:
                            try:
                                user_tweets = self.search_tweets(f"from:{parent_user}", count=50)
                                for tweet in user_tweets:
                                    if tweet.get("tweet_id") == tweet_id:
                                        target_tweet = tweet
                                        break
                                if target_tweet:
                                    break
                            except Exception:
                                continue

        if not target_tweet:
            raise LookupError(f"Tweet {tweet_id} was not found or is not publicly accessible")

        if fetch_replies:
            # Do not turn a rate-limit or authentication failure into an empty
            # comments list.  The caller needs to know that comments were not
            # retrieved, rather than treating the response as "no comments".
            target_tweet["replies_data"] = self.extract_replies(
                url_or_id,
                max_replies=max_replies,
            )

        return target_tweet

    def extract_replies(self, url_or_id: str, max_replies: int = 100, max_depth: Optional[int] = None,
                        include_retweets: bool = False) -> List[Dict[str, Any]]:
        tweet_id = self.extract_tweet_id(url_or_id)
        if not tweet_id:
            raise ValueError("Expected a valid Twitter/X status URL or numeric tweet ID")
        depth_limit = self.config.max_reply_depth if max_depth is None else max_depth
        rows = self._rows(self._call("search", f"conversation_id:{tweet_id}", limit=max_replies + 1, save=False))
        replies: List[Dict[str, Any]] = []
        for row in rows:
            reply = self.normalize_tweet(row)
            if reply["tweet_id"] == tweet_id or (reply["is_retweet"] and not include_retweets):
                continue
            parent = str(reply.get("in_reply_to_id") or tweet_id)
            reply["parent_tweet_id"] = parent
            reply["depth"] = min(self._reply_depth(reply, parent, rows, tweet_id), depth_limit)
            if reply["depth"] <= depth_limit:
                replies.append(reply)
            if len(replies) >= max_replies:
                break
        return replies

    @staticmethod
    def _reply_depth(reply: Mapping[str, Any], parent: str, rows: Sequence[Mapping[str, Any]], root: str) -> int:
        depth, seen = 1, {reply.get("tweet_id")}
        while parent != root and parent and depth < 100:
            if parent in seen:
                break
            seen.add(parent)
            parent_row = next((row for row in rows if str(row.get("tweet_id", row.get("id", ""))) == parent), None)
            if not parent_row:
                break
            parent = str(parent_row.get("in_reply_to_id", parent_row.get("conversation_id", root)))
            depth += 1
        return depth

    def get_profile(self, username: str) -> Dict[str, Any]:
        username = username.lstrip("@").strip()
        if not self.USERNAME.fullmatch(username):
            raise ValueError("Username must contain 1-15 letters, numbers, or underscores")
        
        rows = []
        try:
            rows = self._rows(self._call("get_user_info", [username]))
        except Exception as err:
            self.logger.warning("get_user_info failed for @%s: %s", username, err)
            
        if rows:
            row = rows[0]
            return {
                "username": self._first(row, "username", "screen_name", "user_screen_name", default=username),
                "display_name": self._first(row, "display_name", "name", "user_name"),
                "bio": self._first(row, "bio", "description", default=""),
                "followers": self._first(row, "followers", "followers_count", default=0),
                "following": self._first(row, "following", "following_count", "friends_count", default=0),
                "tweet_count": self._first(row, "tweet_count", "statuses_count", default=0),
                "join_date": self._first(row, "join_date", "created_at"),
                "profile_image_url": self._first(row, "profile_image_url", "profile_image"),
                "banner_image_url": self._first(row, "banner_image_url", "profile_banner_url", "banner"),
                "verified": bool(self._first(row, "verified", "is_verified", default=False)),
                "location": self._first(row, "location"),
                "website": self._first(row, "website", "url"),
                "raw": row,
            }
        
        tweets = self.search_tweets(f"from:{username}", count=10)
        if tweets:
            for tweet in tweets:
                raw = tweet.get("raw") or {}
                user_res = (
                    raw.get("core", {}).get("user_results", {}).get("result", {})
                    or raw.get("user_results", {}).get("result", {})
                )
                legacy = user_res.get("legacy", {})
                core = user_res.get("core", {})
                if legacy or core:
                    return {
                        "username": legacy.get("screen_name") or core.get("screen_name") or username,
                        "display_name": core.get("name") or legacy.get("name") or tweet.get("author_display_name"),
                        "bio": legacy.get("description") or "",
                        "followers": legacy.get("followers_count", 0),
                        "following": legacy.get("friends_count", 0),
                        "tweet_count": legacy.get("statuses_count", 0),
                        "join_date": core.get("created_at") or legacy.get("created_at"),
                        "profile_image_url": user_res.get("avatar", {}).get("image_url") or legacy.get("profile_image_url_https"),
                        "banner_image_url": legacy.get("profile_banner_url"),
                        "verified": bool(legacy.get("verified") or user_res.get("is_blue_verified")),
                        "location": legacy.get("location") or "",
                        "website": legacy.get("url") or "",
                        "raw": user_res,
                    }
            first_tweet = tweets[0]
            return {
                "username": first_tweet.get("author_username") or username,
                "display_name": first_tweet.get("author_display_name"),
                "bio": "",
                "followers": 0,
                "following": 0,
                "tweet_count": 0,
                "join_date": None,
                "profile_image_url": None,
                "banner_image_url": None,
                "verified": False,
                "location": "",
                "website": "",
                "raw": {},
            }
        
        raise LookupError(f"Profile @{username} was not found or is not publicly accessible")

    def get_user_posts(
        self,
        username: str,
        count: int = 100,
        include_replies: bool = True,
        max_replies: int = 100,
    ) -> List[Dict[str, Any]]:
        """Fetch recent posts from a user and their replies/comments."""

        username = username.lstrip("@").strip()

        if not self.USERNAME.fullmatch(username):
            raise ValueError(
                "Username must contain 1-15 letters, numbers, or underscores"
            )

        if count < 1:
            raise ValueError("count must be at least 1")

        posts = []

        try:
            rows = self._rows(
                self._call(
                    "get_profile_tweets",
                    [username],
                    limit=count,
                )
            )

            posts = [
                self.normalize_tweet(row)
                for row in rows[:count]
            ]

        except Exception as err:
            self.logger.warning(
                "get_profile_tweets failed for @%s: %s",
                username,
                err,
            )

        if not posts:
            posts = self.search_tweets(
                f"from:{username}",
                count=count,
            )

        # Fetch actual comments/replies for every post
        if include_replies:
            for post in posts:
                tweet_id = post.get("tweet_id")

                if not tweet_id:
                    post["comments"] = []
                    continue

                # Propagate upstream failures instead of returning partial
                # posts with misleading empty comment lists.
                post["comments"] = self.extract_replies(
                    tweet_id,
                    max_replies=max_replies,
                )

        self.logger.info(
            "Fetched %d recent posts for @%s",
            len(posts),
            username,
        )

        return posts

    def search_tweets(self, query: str, since: Optional[str] = None, until: Optional[str] = None,
                      count: int = 100, sort: str = "relevance") -> List[Dict[str, Any]]:
        kwargs: Dict[str, Any] = {"limit": count, "save": False}
        if since:
            kwargs["since"] = since
        if until:
            kwargs["until"] = until
        if sort in {"relevance", "recency"}:
            kwargs["display_type"] = "Latest" if sort == "recency" else "Top"
        return [self.normalize_tweet(row) for row in self._rows(self._call("search", query, **kwargs))]

    def get_trending_topics(self, location: Optional[str] = None) -> List[str]:
        client = self._build_client()
        if not hasattr(client, "get_trends") and not hasattr(client, "trends"):
            self.logger.warning("This Scweet version does not expose a trends endpoint")
            return []
        method = "get_trends" if hasattr(client, "get_trends") else "trends"
        rows = self._rows(self._call(method, location) if location else self._call(method))
        return [str(self._first(row, "name", "trend", "topic", default="")) for row in rows if self._first(row, "name", "trend", "topic")]

    @staticmethod
    def summary_statistics(tweets: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
        rows = list(tweets)
        return {
            "tweet_count": len(rows),
            "total_likes": sum(int(row.get("likes") or 0) for row in rows),
            "total_retweets": sum(int(row.get("retweets") or 0) for row in rows),
            "total_replies": sum(int(row.get("replies") or 0) for row in rows),
            "unique_authors": len({row.get("author_username") for row in rows if row.get("author_username")}),
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def export(self, data: Any, output: str | Path, format_name: Optional[str] = None) -> List[Path]:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fmt = (format_name or output_path.suffix.lstrip(".") or "json").lower()
        rows = data if isinstance(data, list) else [data]
        records = [dict(row) for row in rows]
        for record in records:
            if "raw" in record:
                record.pop("raw", None)
        if fmt == "json":
            output_path.write_text(json.dumps(records if isinstance(data, list) else records[0], indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        elif fmt == "csv":
            pd.DataFrame(records).to_csv(output_path, index=False)
        elif fmt in {"xlsx", "excel"}:
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                pd.DataFrame(records).to_excel(writer, sheet_name="tweets", index=False)
                pd.DataFrame([self.summary_statistics(records)]).to_excel(writer, sheet_name="summary", index=False)
        else:
            raise ValueError("format must be json, csv, or excel")
        self.logger.info("Exported %d records to %s", len(records), output_path)
        return [output_path]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrape public Twitter/X posts with Scweet")
    parser.add_argument("--auth-token", help="X auth_token cookie; prefer the TWITTER_AUTH_TOKEN environment variable")
    parser.add_argument("--config", default="twitter_config.json")
    parser.add_argument("--url")
    parser.add_argument("--user")
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--posts", action="store_true", help="Fetch recent posts for --user")
    parser.add_argument("--with-replies", action="store_true")
    parser.add_argument("--max-replies", type=int, default=100)
    parser.add_argument("--search")
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--sort", choices=["relevance", "recency"], default="relevance")
    parser.add_argument("--output", default="data/twitter/twitter_results.json")
    parser.add_argument("--format", choices=["json", "csv", "excel"], default=None)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    config_path = Path(args.config)
    config = TwitterConfig.from_file(config_path) if config_path.exists() else TwitterConfig()
    import os
    scraper = TwitterScraper(auth_token=args.auth_token or os.getenv("TWITTER_AUTH_TOKEN"), config=config)
    try:
        if args.profile:
            if not args.user:
                raise SystemExit("--profile requires --user")
            result: Any = scraper.get_profile(args.user)
        elif args.posts:
            if not args.user:
                raise SystemExit("--posts requires --user")
            result = scraper.get_user_posts(args.user, args.count)
        elif args.search:
            result = scraper.search_tweets(args.search, args.since, args.until, args.count, args.sort)
        elif args.url:
            result = scraper.extract_post(args.url)
            if args.with_replies:
                result["replies_data"] = scraper.extract_replies(args.url, args.max_replies)
        else:
            raise SystemExit("Provide --url, --user --profile, or --search")
        scraper.export(result, args.output, args.format)
        return 0
    finally:
        scraper.close()


if __name__ == "__main__":
    raise SystemExit(main())
