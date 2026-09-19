import json

import pytest

from app.services.twitter_service import TwitterService


class DummyScraper:
    def search_tweets(self, *args, **kwargs):
        return [
            {
                "tweet_id": "12345",
                "text": "hello world",
                "author_username": "alice",
                "timestamp": "2026-09-19T12:00:00Z",
                "likes": 5,
                "retweets": 2,
                "replies": 1,
            }
        ]


@pytest.mark.asyncio
async def test_twitter_search_saves_payload_to_data_twitter_file(tmp_path, monkeypatch):
    service = TwitterService()
    monkeypatch.setattr(service, "_build_scraper", lambda: DummyScraper())
    monkeypatch.setattr("app.services.twitter_service.ROOT_DIR", tmp_path)

    result = await service.search_tweets("hello", max_results=10)

    assert "saved_file" in result
    saved_file = result["saved_file"]
    assert saved_file.startswith(str(tmp_path / "data" / "Twitter"))

    payload = json.loads(open(saved_file, "r", encoding="utf-8").read())
    assert payload["query"] == "hello"
    assert payload["total"] == 1
    assert payload["results"][0]["text"] == "hello world"
