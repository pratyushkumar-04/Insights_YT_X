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
async def test_twitter_search_returns_payload_in_response(monkeypatch):
    service = TwitterService()
    monkeypatch.setattr(service, "_build_scraper", lambda: DummyScraper())

    result = await service.search_tweets("hello", max_results=10)

    assert "saved_file" not in result
    assert result["query"] == "hello"
    assert result["total"] == 1
    assert result["results"][0]["text"] == "hello world"
