"""Test caching."""
import time
from unittest.mock import patch

from fastapi.testclient import TestClient

from proxy_server.api.dependencies import cached_responses

from tests.test_request import MAX_PAGES

# pylint: disable=protected-access

TEN_SECONDS_CACHE = 10


def test_cache_responses(client: TestClient, path_url: str):
    """Test that responses are being cached,
    and the response time is shorter as a result."""
    response_page = client.get(path_url.format(2))._elapsed.total_seconds()
    response_pages_after_wait = client.get(path_url.format(2))._elapsed.total_seconds()
    assert response_pages_after_wait < response_page


def test_ttl_per_item(client: TestClient, path_url: str):
    """Test expire time being unique per item.."""
    with patch.object(cached_responses, "DAY_CACHE_IN_SECONDS", TEN_SECONDS_CACHE):
        client.get(path_url.format(MAX_PAGES))._elapsed.total_seconds()
        time.sleep(TEN_SECONDS_CACHE / 2)

        # Without a query param.
        response = client.get(path_url)._elapsed.total_seconds()
        time.sleep(TEN_SECONDS_CACHE / 2 + 1)  # suppress the cache time.

        expired_response_after_wait = client.get(
            path_url.format(MAX_PAGES)
        )._elapsed.total_seconds()
        response_after_wait = client.get(path_url)._elapsed.total_seconds()
    assert response_after_wait < expired_response_after_wait
    assert response_after_wait < response
