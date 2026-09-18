import pytest

from app.services.twitter_service import TwitterService


@pytest.mark.asyncio
async def test_get_tweet_fetches_and_returns_comments(monkeypatch) -> None:
    """The tweet endpoint must opt in to the scraper's reply collection."""

    captured = {}

    class FakeScraper:
        def extract_post(self, tweet_id: str, fetch_replies: bool = False):
            captured["tweet_id"] = tweet_id
            captured["fetch_replies"] = fetch_replies
            return {
                "tweet_id": tweet_id,
                "text": "Root post",
                "author_username": "author",
                "replies_data": [{"tweet_id": "reply-1", "text": "A reply"}],
            }

    service = TwitterService()
    monkeypatch.setattr(service, "_build_scraper", lambda: FakeScraper())

    result = await service.get_tweet_by_id("123456789")

    assert captured == {"tweet_id": "123456789", "fetch_replies": True}
    assert result["comments"] == [{"tweet_id": "reply-1", "text": "A reply"}]
