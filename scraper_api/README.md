# Scraper API

A FastAPI service that exposes wrappers around the existing YouTube, Twitter/X, and Telegram scraping modules.

## Features

- YouTube video, channel, and batch extraction endpoints
- Twitter/X search, user, and tweet routes
- Telegram channel message retrieval routes
- Structured logging and error handling
- API key support and rate limiting
- Docker-ready deployment structure

## Quick start

```bash
cd scraper_api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment

Create a `.env` file using the sample below:

```env
APP_NAME=Scraper API
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
REQUIRE_API_KEY=false
API_KEYS=demo-key-1,demo-key-2
RATE_LIMIT_ENABLED=true
LOG_LEVEL=INFO
```

## Endpoints

### Health

- `GET /health`
- `GET /`

### YouTube

- `POST /youtube/video`
- `POST /youtube/channel`
- `POST /youtube/batch`

### Twitter/X

- `POST /twitter/search`
- `POST /twitter/user`
- `POST /twitter/tweet`

### Telegram

- `POST /telegram/channel`

## Example requests

### YouTube video

```bash
curl -X POST http://localhost:8000/youtube/video \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "include_comments": false,
    "include_transcript": false
  }'
```

### Twitter search

```bash
curl -X POST http://localhost:8000/twitter/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenAI",
    "max_results": 10
  }'
```

### Telegram channel

```bash
curl -X POST http://localhost:8000/telegram/channel \
  -H "Content-Type: application/json" \
  -d '{
    "channel_name": "example_channel",
    "limit": 20
  }'
```

## Docker

```bash
docker build -t scraper-api .
docker run --rm -p 8000:8000 scraper-api
```
