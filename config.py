import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# yt-dlp settings
YDL_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,
    'ignoreerrors': True,
    'no_check_certificate': True,
    'prefer_insecure': False,
    'geo_bypass': True,
    'socket_timeout': 30,
}

# Analysis settings
MAX_COMMENTS_PER_VIDEO = 100
BATCH_DELAY_SECONDS = 2
ENGAGEMENT_WEIGHTS = {
    'like': 1.0,
    'comment': 2.0,
}

# Sentiment thresholds
POSITIVE_THRESHOLD = 0.1
NEGATIVE_THRESHOLD = -0.1

# Common stopwords for keyword analysis
STOPWORDS = {'the', 'to', 'for', 'of', 'on', 'at', 'by', 'in', 'a', 'an',
             'and', 'or', 'but', 'is', 'are', 'was', 'were', 'with', 'without'}
