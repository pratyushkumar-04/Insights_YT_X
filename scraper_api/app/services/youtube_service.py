"""Service layer for YouTube scraping operations."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

from app.core.logging import get_logger
from app.exceptions import ScraperUpstreamError, ScraperValidationError

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.utils import get_video_id_from_url
from src.youtube_extractor import YouTubeExtractor, get_channel_video_urls

logger = get_logger(__name__)


class YouTubeService:
    """Thin wrapper around the existing project scraper logic."""

    @staticmethod
    def _normalize_video(video_result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "video_id": video_result.get("video_id") or "",
            "title": video_result.get("title") or "",
            "channel": video_result.get("uploader") or video_result.get("channel") or None,
            "channel_id": video_result.get("channel_id") or None,
            "description": video_result.get("description") or None,
            "duration": video_result.get("duration_string") or video_result.get("duration") or None,
            "published_at": video_result.get("upload_date") or None,
            "view_count": video_result.get("view_count") or 0,
            "like_count": video_result.get("like_count") or 0,
            "comment_count": video_result.get("comment_count") or 0,
            "thumbnail_url": video_result.get("thumbnail") or None,
            "raw_data": video_result,
        }

    async def extract_video(self, video_url: str, include_comments: bool = False, include_transcript: bool = False) -> Dict[str, Any]:
        """Extract a single video using the existing scraper module."""
        try:
            video_id = get_video_id_from_url(video_url)
            if not video_id:
                raise ScraperValidationError("A valid YouTube video URL or ID is required.")

            extractor = YouTubeExtractor()
            video = extractor.get_video_data(video_id, fetch_comments=include_comments)
            if "error" in video:
                raise ScraperUpstreamError(str(video.get("error", "Failed to extract YouTube video data")))

            if include_transcript:
                transcript = extractor.get_transcript(video_id)
                video["transcript"] = transcript

            logger.info("youtube_extract_video", video_id=video_id, include_comments=include_comments)
            return self._normalize_video(video)
        except ScraperValidationError:
            raise
        except Exception as exc:
            logger.exception("youtube_extract_video_failed", exc_info=exc)
            raise ScraperUpstreamError("Failed to extract YouTube video data") from exc

    async def extract_channel(self, channel_url: str, max_videos: int = 5, include_comments: bool = False) -> Dict[str, Any]:
        """Extract all videos from a YouTube channel."""
        try:
            if not channel_url:
                raise ScraperValidationError("A valid YouTube channel URL or handle is required.")

            video_urls = get_channel_video_urls(channel_url, max_videos=min(max_videos, 5))
            if not video_urls:
                raise ScraperValidationError("No videos were found for the supplied channel.")

            extractor = YouTubeExtractor()
            videos = []
            for video_url in video_urls[:5]:
                video_id = get_video_id_from_url(video_url)
                if not video_id:
                    continue
                raw = extractor.get_video_data(video_id, fetch_comments=include_comments)
                if "error" not in raw:
                    videos.append(self._normalize_video(raw))

            logger.info("youtube_extract_channel", channel_url=channel_url, count=len(videos))
            return {
                "channel_id": None,
                "channel_name": channel_url,
                "videos": videos,
                "total_videos": len(videos),
                "raw_data": {"source_url": channel_url, "video_urls": video_urls},
            }
        except ScraperValidationError:
            raise
        except Exception as exc:
            logger.exception("youtube_extract_channel_failed", exc_info=exc)
            raise ScraperUpstreamError("Failed to extract YouTube channel data") from exc

    async def extract_batch(self, video_urls: List[str], include_comments: bool = False) -> Dict[str, Any]:
        """Extract a batch of YouTube videos."""
        try:
            if not video_urls:
                raise ScraperValidationError("At least one YouTube URL is required for batch extraction.")

            extractor = YouTubeExtractor()
            videos = []
            for video_url in video_urls[:5]:
                video_id = get_video_id_from_url(video_url)
                if not video_id:
                    continue
                raw = extractor.get_video_data(video_id, fetch_comments=include_comments)
                if "error" not in raw:
                    videos.append(self._normalize_video(raw))

            logger.info("youtube_extract_batch", count=len(videos))
            return {"videos": videos, "total": len(videos)}
        except ScraperValidationError:
            raise
        except Exception as exc:
            logger.exception("youtube_extract_batch_failed", exc_info=exc)
            raise ScraperUpstreamError("Failed to extract YouTube batch") from exc


youtube_service = YouTubeService()
