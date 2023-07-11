"""Basic test fixtures."""
import pytest

from cachetools import TTLCache

from fastapi.testclient import TestClient

from slowapi import Limiter
from slowapi.util import get_remote_address

from proxy_server.api.app import app, MAX_REQUESTS_PER_MINUTE
from proxy_server.api.dependencies.cached_responses import MAX_REQUESTS_PER_DAY
from proxy_server.api.dependencies.cached_responses import responses_cache


# pylint: disable=redefined-outer-name

OVERHEAD = 2  # Overhead to add to by day max limit.
TEN_SECONDS_CACHE = 10


@pytest.fixture
def client():
    """Test client."""
    yield TestClient(app)
    app.state.limiter.reset()  # For limit testing.
    responses_cache().clear()  # For cache testing


@pytest.fixture
def example_url():
    """Example url from exercise demands."""
    return "https://reqres.in/api/users?page={}"  # example url supplied.


@pytest.fixture()
def path_url(example_url):
    """Example api path with correct formatting to out api."""
    return f"/{example_url}"


@pytest.fixture()
def mock_limiter():
    """Mocks the app's limiter to block on second instead of minute."""
    limits = [f"{MAX_REQUESTS_PER_MINUTE}/second"]
    return Limiter(key_func=get_remote_address, default_limits=limits)


@pytest.fixture
def mock_cache():
    """Create a cache with less ttl."""
    return TTLCache(maxsize=MAX_REQUESTS_PER_DAY,
                    ttl=TEN_SECONDS_CACHE)


@pytest.fixture(autouse=True)
def override_cache(mock_cache):
    """Override the cache dependency"""
    app.dependency_overrides[responses_cache] = lambda : mock_cache
