"""Basic test fixtures."""
import pytest

from fastapi.testclient import TestClient


from slowapi import Limiter
from slowapi.util import get_remote_address

from proxy_server.api.app import app, LIMITS, MAX_REQUESTS_PER_MINUTE

# pylint: disable=redefined-outer-name

OVERHEAD = 2  # Overhead of requests to add to max_requests per minute.


@pytest.fixture
def client():
    """Test client."""
    yield TestClient(app)
    app.state.limiter.reset()  # For limit testing.


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
    """Mocks the app's limiter less messages per day."""
    limits = LIMITS
    limits[1] = f"{MAX_REQUESTS_PER_MINUTE + OVERHEAD}/day"
    return Limiter(key_func=get_remote_address, default_limits=limits)
