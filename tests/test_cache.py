"""Test caching."""
import pytest
import time

from unittest.mock import patch

import aiohttp

from fastapi.testclient import TestClient

from proxy_server.api.dependencies import cached_responses

from tests.test_request import MAX_PAGES
from tests.conftest import TEN_SECONDS_CACHE

# pylint: disable=protected-access


def test_cached(client: TestClient,
                      path_url: str,
                      mocker):
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
    with patch.object(cached_responses, "DAY_CACHE_IN_SECONDS", TEN_SECONDS_CACHE):
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

