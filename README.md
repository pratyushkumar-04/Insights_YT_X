# 🚀 YouTube & Twitter/X Influencer Data Scraper

A high-performance Python toolkit for extracting raw public details, engagement statistics, video metadata, comments, and user timelines from **YouTube** and **Twitter/X**. 

This tool extracts structured data into JSON/CSV/Excel format so it can be fed directly into **AI models**, **NLP sentiment analyzers**, or **influencer growth insight pipelines**.

---

## 📋 Features

### 📺 YouTube Extractor
- **Single Video Data**: Extracts full metadata (views, likes, duration, tags, uploader, upload date) and top comments (limited efficiently via `yt-dlp`).
- **Flexible URL & ID Parsing**: Supports standard YouTube watch URLs (`youtube.com/watch?v=`), Shorts (`youtube.com/shorts/`), Embed links, `youtu.be/` links, and raw 11-char video IDs.
- **Channel Extraction**: Fetches video lists for any channel using handles (e.g. `@MrBeast` or `MrBeast`), custom channel URLs, or channel IDs.
- **Batch Processing**: Extracts data for multiple videos in parallel/batches with automated rate limiting and progress bars.

### 🐦 Twitter/X Scraper
- **User Profile Scraper**: Extracts follower/following counts, bio, profile/banner image URLs, join dates, and verification status.
- **User Timeline Scraper**: Retrieves recent tweets for any public user profile.
- **Single Tweet & Comments Extractor**: Scrapes tweet contents, engagement metrics (likes, retweets, replies), media links, and reply threads/comments (`replies_data`) via tweet URL or status ID.
- **Keyword & Topic Search**: Performs targeted keyword and hashtag searches across X with relevance or recency sorting.
- **Multi-Format Export**: Export results to `JSON`, `CSV`, or `Excel` (`.xlsx`).
- **Resilient Fallback Mechanism**: Automatic fallback strategies and DB account state auto-clean up to prevent token conflicts or local rate limit blocks.

---

## 🛠️ Project Structure

```text
youtube-insights/
├── main.py                     # Primary interactive terminal application
├── scraper.py                  # CLI entry point for standalone Twitter scraping
├── config.py                   # Shared configuration parameters (delays, limits, paths)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules for state DB, environment, and outputs
├── data/                       # Directory for output JSON, CSV, and Excel files
│   ├── twitter/                # Twitter extraction outputs (profile.json, tweet.json, etc.)
│   └── youtube_data_*.json     # YouTube extraction outputs
└── src/                        # Core extraction & analysis packages
    ├── youtube_extractor.py    # YouTube metadata & channel scraping logic
    ├── twitter_scraper.py      # Twitter/X scraping & normalization module
    ├── data_analyzer.py        # Pandas & TextBlob analysis module
    ├── insights_generator.py   # AI growth insight generator module
    └── utils.py                # Regex URL parsers and string helpers
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- **Python 3.10** or higher installed.

### 2. Environment Setup
Clone or extract the repository, navigate into the folder, and create a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Interactive CLI Usage (`main.py`)

Run the main application:

```bash
python main.py
```

### Menu Options

```text
============================================================
🚀 YOUTUBE CREATOR GROWTH INSIGHTS TOOL
============================================================

What would you like to do?
1. Extract data from a single video
2. Extract data from a channel (by handle)
3. Extract data from Twitter/X
4. Exit
```

---

### Option 1: Extract Data from a Single YouTube Video
1. Enter any YouTube Video URL or Video ID. Supported input formats:
   - `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - `https://youtu.be/dQw4w9WgXcQ`
   - `https://www.youtube.com/shorts/dQw4w9WgXcQ`
   - `dQw4w9WgXcQ`
2. Choose whether to fetch comments (`y/n`, default: `y`).
3. Output is printed to terminal and saved to `data/youtube_data_YYYYMMDD_HHMMSS.json`.

---

### Option 2: Extract Data from a YouTube Channel
1. Enter a channel handle or full channel URL:
   - `@GoogleDevelopers` or `GoogleDevelopers`
   - `https://www.youtube.com/@Google`
2. Specify the maximum number of videos to fetch (or press Enter for all).
3. Choose whether to fetch comments per video (`y/n`, default: `n`).
4. Output is saved to `data/youtube_data_YYYYMMDD_HHMMSS.json`.

---

### Option 3: Extract Data from Twitter/X
1. Enter your Twitter/X `auth_token` cookie when prompted (or set `TWITTER_AUTH_TOKEN` environment variable).
2. Select an action from the Twitter sub-menu:
   - **1. Get user profile**: Enter username (e.g. `elonmusk`).
   - **2. Get recent posts for a user**: Enter username & post limit.
   - **3. Get tweet by URL or ID**: Enter tweet status URL or ID and toggle comment/reply extraction (`y/n`, default: `y`).
   - **4. Search tweets**: Enter query string & result count.
   - **5. Back**: Return to main menu.
3. Outputs are saved under `data/twitter/`.

---

## 💻 Standalone Twitter CLI (`scraper.py`)

You can also run Twitter extractions directly via command line arguments:

### 1. Fetch User Profile
```bash
python scraper.py --auth-token "YOUR_AUTH_TOKEN" --user elonmusk --profile --output data/twitter/elonmusk_profile.json --format json
```

### 2. Fetch User Posts
```bash
python scraper.py --auth-token "YOUR_AUTH_TOKEN" --user elonmusk --posts --count 50 --output data/twitter/elonmusk_posts.json --format json
```

### 3. Fetch Single Tweet with Comments/Replies
```bash
python scraper.py --auth-token "YOUR_AUTH_TOKEN" --url "https://x.com/ImRaina/status/2100452295129612569" --with-replies --max-replies 50 --output data/twitter/tweet.json --format json
```

### 4. Search Tweets
```bash
python scraper.py --auth-token "YOUR_AUTH_TOKEN" --search "artificial intelligence" --count 50 --sort recency --output data/twitter/search_ai.csv --format csv
```

---

## 🐍 Programmatic API Usage for Developers

If you are developing downstream AI models or pipeline scripts, you can import the Python extractor classes directly:

### 1. Extracting YouTube Data in Python
```python
from src.youtube_extractor import YouTubeExtractor, get_channel_video_urls
from src.utils import get_video_id_from_url

extractor = YouTubeExtractor()

# Single Video
video_id = get_video_id_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
video_data = extractor.get_video_data(video_id, fetch_comments=True)
print("Title:", video_data.get("title"))
print("Comments fetched:", len(video_data.get("comments", [])))

# Channel Video URLs
video_urls = get_channel_video_urls("@Google", max_videos=10)
video_ids = [get_video_id_from_url(url) for url in video_urls]

# Batch Extract
batch_data = extractor.batch_extract(video_ids, fetch_comments=False)
```

### 2. Extracting Twitter/X Data with Comments in Python
```python
from src.twitter_scraper import TwitterScraper

AUTH_TOKEN = "your_auth_token_here"
scraper = TwitterScraper(auth_token=AUTH_TOKEN)

try:
    # 1. Fetch Profile
    profile = scraper.get_profile("elonmusk")
    print(f"Followers: {profile['followers']:,}")

    # 2. Fetch User Posts
    posts = scraper.get_user_posts("elonmusk", count=20)
    for p in posts:
        print(p["tweet_id"], p["text"])

    # 3. Fetch Tweet WITH Comments/Replies
    tweet = scraper.extract_post("https://x.com/ImRaina/status/2100452295129612569", fetch_replies=True, max_replies=50)
    print("Tweet:", tweet["text"])
    print("Comments/Replies fetched:", len(tweet.get("replies_data", [])))

    # 4. Search Tweets
    search_results = scraper.search_tweets("Generative AI", count=30)
    
    # 5. Export Data
    scraper.export(tweet, "data/twitter/tweet.json", format_name="json")
finally:
    scraper.close()
```

---

## 📊 Data Schema Reference

### YouTube Output (`youtube_data_*.json`)
```json
{
  "dQw4w9WgXcQ": {
    "video_id": "dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up",
    "description": "The official video for Never Gonna Give You Up...",
    "view_count": 1500000000,
    "like_count": 17000000,
    "comment_count": 2200000,
    "upload_date": "20091025",
    "uploader": "Rick Astley",
    "channel_id": "UCuAXFkgsw1L7xaCfnd5JJOw",
    "duration": 213,
    "duration_string": "03:33",
    "tags": ["Rick Astley", "Never Gonna Give You Up"],
    "categories": ["Music"],
    "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "comments": [
      {
        "author": "User Name",
        "author_id": "@username",
        "text": "Great song!",
        "like_count": 150,
        "time_text": "2 days ago",
        "reply_count": 3
      }
    ]
  }
}
```

### Twitter/X Single Tweet with Comments Output (`tweet.json`)
```json
{
  "tweet_id": "2100452295129612569",
  "text": "இனிய பிறந்தநாள் வாழ்த்துகள், @ashwinravi99! 🎂🇮🇳...",
  "author_username": "ImRaina",
  "author_display_name": "Suresh Raina🇮🇳",
  "timestamp": "Thu Sep 17 05:10:26 +0000 2026",
  "likes": 13223,
  "retweets": 809,
  "replies": 46,
  "views": 0,
  "hashtags": [],
  "mentions": ["ashwinravi99"],
  "image_urls": ["https://pbs.twimg.com/media/HSZOOjeaIAEJ39V.jpg"],
  "video_urls": [],
  "url": "https://x.com/ImRaina/status/2100452295129612569",
  "replies_data": [
    {
      "tweet_id": "2100465858036527313",
      "text": "@ImRaina @ashwinravi99 Tamil 😮🔥🔥🥹",
      "author_username": "Crazyydas",
      "author_display_name": "Mohan Ji ツᶜˢᴷ",
      "timestamp": "Thu Sep 17 06:04:19 +0000 2026",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "parent_tweet_id": "2100452295129612569",
      "depth": 1
    }
  ]
}
```

### Twitter/X Profile Output (`profile.json`)
```json
{
  "username": "elonmusk",
  "display_name": "Elon Musk",
  "bio": "https://t.co/ZdBx5WABYx",
  "followers": 241643635,
  "following": 1406,
  "tweet_count": 108689,
  "join_date": "Tue Jun 02 20:12:29 +0000 2009",
  "profile_image_url": "https://pbs.twimg.com/profile_images/...",
  "banner_image_url": "https://pbs.twimg.com/profile_banners/...",
  "verified": true,
  "location": "",
  "website": ""
}
```

---

## 🔑 Obtaining Twitter/X `auth_token`

To scrape Twitter/X using authenticated requests:
1. Open Twitter/X ([x.com](https://x.com)) in your browser and log in.
2. Open Developer Tools (`F12` or `Ctrl+Shift+I`) and go to the **Application** tab (or **Storage** in Firefox).
3. Expand **Cookies** and select `https://x.com`.
4. Copy the value of the `auth_token` cookie.
5. Provide it in the prompt or set it in your environment:
   ```bash
   # Windows PowerShell
   $env:TWITTER_AUTH_TOKEN="your_auth_token_here"

   # Linux/macOS
   export TWITTER_AUTH_TOKEN="your_auth_token_here"
   ```

---

## ❓ Troubleshooting & Tips

- **Fast YouTube Comments Fetching**: The scraper enforces `max_comments` at the extraction level (`extractor_args`), ensuring comment collection finishes quickly without downloading millions of comments.
- **Twitter Account State Cleanup**: If you switch tokens or hit rate limits, `TwitterScraper` automatically cleans stale token states from `scweet_state.db`.
- **Output Files**: All generated JSON/CSV/Excel output files are saved under the `data/` folder.
