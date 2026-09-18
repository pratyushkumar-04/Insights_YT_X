import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import yt_dlp
from colorama import Fore, init
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))
from config import BATCH_DELAY_SECONDS, DATA_DIR, MAX_COMMENTS_PER_VIDEO, YDL_OPTS

init(autoreset=True)


class YouTubeExtractor:
    """Main class for extracting YouTube video data using yt-dlp."""

    def __init__(self, opts: Dict = None):
        self.opts = opts or YDL_OPTS.copy()

    def get_video_data(self, video_id: str, fetch_comments: bool = True) -> Dict:
        """Extract complete data for a single video."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"{Fore.CYAN}Fetching data for video: {video_id}")
        opts = self.opts.copy()
        if fetch_comments:
            opts['getcomments'] = True
            opts['extractor_args'] = {'youtube': {'max_comments': [str(MAX_COMMENTS_PER_VIDEO)]}}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return {'error': f'No data found for video {video_id}'}
                result = self._extract_metadata(info)
                result['comments'] = self._extract_comments(info) if fetch_comments else []
                print(f"{Fore.GREEN}Successfully fetched: {result['title'][:50]}...")
                return result
        except Exception as e:
            error_msg = str(e)
            print(f"{Fore.RED}Error: {error_msg}")
            return {'error': error_msg, 'video_id': video_id}

    def _extract_metadata(self, info: Dict) -> Dict:
        """Extract metadata from yt-dlp info dictionary."""
        return {
            'video_id': info.get('id', 'N/A'), 'title': info.get('title', 'N/A'),
            'description': info.get('description', 'N/A'), 'view_count': info.get('view_count', 0),
            'like_count': info.get('like_count', 0), 'dislike_count': info.get('dislike_count', 0),
            'comment_count': info.get('comment_count', 0), 'upload_date': info.get('upload_date', 'N/A'),
            'uploader': info.get('uploader', 'N/A'), 'channel_id': info.get('channel_id', 'N/A'),
            'channel_url': info.get('channel_url', 'N/A'), 'duration': info.get('duration', 0),
            'duration_string': self._format_duration(info.get('duration', 0)), 'tags': info.get('tags', []),
            'categories': info.get('categories', []), 'thumbnail': info.get('thumbnail', 'N/A'),
            'webpage_url': info.get('webpage_url', 'N/A'),
            'subtitles_available': list(info.get('subtitles', {}).keys()),
            'automatic_captions': list(info.get('automatic_captions', {}).keys()),
            'average_rating': info.get('average_rating', 0), 'age_limit': info.get('age_limit', 0),
            'is_live': info.get('is_live', False), 'was_live': info.get('was_live', False),
        }

    def _extract_comments(self, info: Dict) -> List[Dict]:
        """Extract and format comments from info dictionary."""
        comments = []
        for comment in info.get('comments', [])[:MAX_COMMENTS_PER_VIDEO]:
            try:
                comments.append({
                    'author': comment.get('author', 'N/A'), 'author_id': comment.get('author_id', 'N/A'),
                    'text': comment.get('text', 'N/A'), 'like_count': comment.get('like_count', 0),
                    'timestamp': comment.get('timestamp', None), 'time_text': comment.get('time_text', 'N/A'),
                    'is_pinned': comment.get('is_pinned', False), 'is_hearted': comment.get('is_hearted', False),
                    'reply_count': comment.get('reply_count', 0),
                })
            except Exception:
                continue
        return comments

    def _format_duration(self, seconds: int) -> str:
        """Convert seconds to HH:MM:SS format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds %= 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"

    def batch_extract(self, video_ids: List[str], fetch_comments: bool = True) -> Dict:
        """Extract data for multiple videos with progress bar."""
        results = {}
        print(f"\n{Fore.YELLOW}Starting batch extraction for {len(video_ids)} videos...\n")
        with tqdm(total=len(video_ids), desc="Extracting videos", unit="video") as pbar:
            for index, video_id in enumerate(video_ids, 1):
                data = self.get_video_data(video_id, fetch_comments)
                results[video_id] = data
                pbar.update(1)
                pbar.set_postfix({'Current': video_id[:8], 'Comments': len(data.get('comments', []))})
                if index < len(video_ids):
                    time.sleep(BATCH_DELAY_SECONDS)
        self.save_results(results)
        return results

    def save_results(self, data: Dict, filename: str = None):
        """Save extracted data to JSON file."""
        if not filename:
            import datetime
            filename = f"youtube_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = DATA_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"\n{Fore.GREEN}Data saved to: {filepath}")
        return filepath

    def get_transcript(self, video_id: str, lang: str = 'en') -> Optional[str]:
        """Get transcript/subtitles URL for a video."""
        opts = {'quiet': True, 'writesubtitles': True, 'writeautomaticsub': True,
                'subtitlesformat': 'json3', 'subtitleslangs': [lang]}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                subs = info.get('subtitles', {}).get(lang, []) or info.get('automatic_captions', {}).get(lang, [])
                return subs[0].get('url') if subs else None
        except Exception as e:
            print(f"{Fore.RED}Error fetching transcript: {e}")
            return None


def get_channel_video_urls(channel_input: str, max_videos: Optional[int] = None) -> List[str]:
    """Fetch video URLs from a YouTube channel using its handle or URL."""
    channel_input = channel_input.strip().strip('"\'')
    if not channel_input:
        return []

    if channel_input.startswith('http://') or channel_input.startswith('https://'):
        clean_url = channel_input.rstrip('/')
        if not clean_url.endswith('/videos'):
            channel_url = f"{clean_url}/videos"
        else:
            channel_url = clean_url
    else:
        handle = channel_input if channel_input.startswith('@') else f"@{channel_input}"
        channel_url = f"https://www.youtube.com/{handle}/videos"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
    }
    if max_videos is not None:
        ydl_opts['playlistend'] = max_videos

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
        entries = info.get('entries', []) if info else []
        video_urls = [
            f"https://www.youtube.com/watch?v={entry['id']}"
            for entry in entries
            if entry and entry.get('id')
        ]
        print(f"{Fore.GREEN}Found {len(video_urls)} videos for channel: {channel_input}")
        return video_urls
    except Exception as error:
        print(f"{Fore.RED}Error fetching channel videos: {error}")
        return []

    