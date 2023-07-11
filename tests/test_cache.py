"""Test caching."""
import time

import pytest
import aiohttp

from fastapi.testclient import TestClient


from tests.test_request import MAX_PAGES
from tests.conftest import TEN_SECONDS_CACHE


def test_cached(client: TestClient,
                path_url: str,
                mocker):
    """test that proxy request does take data from cache."""
    response = client.get(path_url.format(MAX_PAGES))
    spy = mocker.spy(aiohttp.ClientSession, "request")
    cached_response = client.get(path_url.format(MAX_PAGES))

    assert response.content == cached_response.content
    with pytest.raises(AssertionError):
        spy.assert_called()
    mocker.stop(spy)


def test_ttl_per_item(client: TestClient,
                      path_url: str,
                      mocker):
    """Test expire time being unique per item."""
    spy = mocker.spy(aiohttp.ClientSession, "request")
    client.get(path_url.format(MAX_PAGES))
    time.sleep(TEN_SECONDS_CACHE / 2)

    # Without a query param.
    client.get(path_url)
    time.sleep(TEN_SECONDS_CACHE / 2 + 1)  # suppress the cache time.
    client.get(
        path_url.format(MAX_PAGES)
    )
    client.get(path_url)
    assert spy.call_count == 3
    mocker.stop(spy)
