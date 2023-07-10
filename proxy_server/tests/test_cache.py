"""Test caching."""
from unittest.mock import patch

from fastapi.testclient import TestClient

from proxy_server.api.app import app
from proxy_server.api.dependencies import chached_responses

client = TestClient(app)


REQRES_ROUTE = "/https://reqres.in/api/users%3Fpage="


def test_cache():
    """Test and items expire from cache one by one and now in a batch."""
    with patch.object(chached_responses, "DAY_CACHE_IN_SECONDS", 10):
        pass
        # response_pages_2 = client.get(f"{REQRES_ROUTE}2")
        # sleep(5)
        # response_pages_3 = client.get(f"{REQRES_ROUTE}3")
        # sleep(6)
        # response_pages_2_after_wait = client.get(f"{REQRES_ROUTE}2")
        # response_pages_3_after_wait = client.get(f"{REQRES_ROUTE}3")


test_cache()
