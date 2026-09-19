import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.twitter_scraper import TwitterConfig, TwitterScraper


def test_scweet_call_makes_at_most_one_retry() -> None:
    calls = 0

    class FailingClient:
        def search(self, *_args, **_kwargs):
            nonlocal calls
            calls += 1
            raise RuntimeError("rate limited")

    scraper = TwitterScraper(
        client=FailingClient(),
        config=TwitterConfig(retry_backoff_seconds=0),
        sleep=lambda _seconds: None,
    )

    try:
        scraper._call("search", "example")
    except RuntimeError:
        pass

    assert calls == 2  # initial attempt plus one retry


def test_scweet_does_not_retry_an_empty_account_pool() -> None:
    calls = 0

    class FailingClient:
        def search(self, *_args, **_kwargs):
            nonlocal calls
            calls += 1
            raise RuntimeError("No eligible accounts (total=0, no accounts in pool)")

    scraper = TwitterScraper(client=FailingClient(), sleep=lambda _seconds: None)

    try:
        scraper._call("search", "example")
    except RuntimeError:
        pass

    assert calls == 1


def test_reply_failure_is_not_reported_as_empty_comments() -> None:
    scraper = TwitterScraper(client=object(), sleep=lambda _seconds: None)
    scraper.extract_replies = lambda *_args, **_kwargs: (_ for _ in ()).throw(
        RuntimeError("rate limited")
    )

    # A post found by the conversation lookup still must expose a reply error.
    scraper._call = lambda *_args, **_kwargs: [
        {"tweet_id": "123456789", "text": "root"}
    ]

    try:
        scraper.extract_post("123456789", fetch_replies=True)
    except RuntimeError as exc:
        assert str(exc) == "rate limited"
    else:  # pragma: no cover - assertion failure path
        raise AssertionError("Reply failures must not be replaced with []")
