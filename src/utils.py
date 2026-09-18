import re
from typing import Optional


def get_video_id_from_url(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats or raw video ID."""
    if not url:
        return None
    url = url.strip().strip('"\'')
    if re.fullmatch(r'[0-9A-Za-z_-]{11}', url):
        return url
    patterns = [
        r'(?:v=|/v/|/embed/|/shorts/|youtu\.be/)([0-9A-Za-z_-]{11})',
        r'(?:v=|/)([0-9A-Za-z_-]{11})(?:[?&]|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def clean_text(text: str) -> str:
    """Clean text by removing special characters and extra spaces."""
    if not text:
        return ""
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

