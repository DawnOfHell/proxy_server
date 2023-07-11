"""Test rate limiting."""
import time
from typing import Callable

import pytest

import requests

from slowapi import Limiter

from fastapi import status
from fastapi.testclient import TestClient

from proxy_server.api.app import app
from proxy_server.api.app import MAX_REQUESTS_PER_MINUTE


from tests.test_request import MAX_PAGES

# pylint: disable=redefined-outer-name


@pytest.fixture
def send_max_minute(client: TestClient, example_url: str, path_url: str):
    """Send the limit of messages that can be sent in one minute."""
    def send():
        real_content = requests.get(example_url.format(MAX_PAGES))
        assert all(client.get(path_url.format(MAX_PAGES)).content == real_content.content
                   for _ in range(MAX_REQUESTS_PER_MINUTE))

    return send


def test_minute_limit_and_unblocking(
    send_max_minute: Callable, client: TestClient, path_url: str, mock_limiter: Limiter
):
    """Test that after a minute passes the user is not blocked."""
    app.state.limiter = mock_limiter
    send_max_minute()
    blocked_content = client.get(path_url.format(MAX_PAGES))
    assert blocked_content.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    time.sleep(1)  # Wait to the end of the block

    proxy_content = client.get(path_url.format(MAX_PAGES))
    assert proxy_content.status_code == status.HTTP_200_OK
