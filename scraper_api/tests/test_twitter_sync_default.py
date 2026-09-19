import types

from src.twitter_scraper import TwitterScraper


class FakeScweetConfig:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeScweet:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.config = kwargs["config"]


def test_twitter_scraper_uses_sync_mode_by_default(monkeypatch):
    fake_module = types.SimpleNamespace(Scweet=FakeScweet, ScweetConfig=FakeScweetConfig)
    monkeypatch.setitem(__import__("sys").modules, "Scweet", fake_module)

    scraper = TwitterScraper(auth_token="abc123")
    client = scraper._build_client()

    assert client.config.api_http_mode == "sync"
