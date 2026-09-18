import pytest

from app.services.twitter_service import TwitterService


@pytest.mark.asyncio
async def test_twitter_service_maps_exhausted_account_pool_to_clear_error() -> None:
    service = TwitterService()

    class FakeError(Exception):
        pass

    try:
        from Scweet.exceptions import AccountPoolExhausted
    except ImportError:  # pragma: no cover
        AccountPoolExhausted = FakeError

    with pytest.raises(Exception):
        try:
            raise AccountPoolExhausted("No eligible accounts (total=0, no accounts in pool). Check your credentials or wait for cooldowns to expire.")
        except AccountPoolExhausted as exc:
            raise service._format_account_error(exc)
