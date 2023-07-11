"""Test rate limiting."""
import time
from typing import Callable

import pytest
import requests
from fastapi import status
from fastapi.testclient import TestClient

from proxy_server.api.app import app
from proxy_server.api.app import MAX_REQUESTS_PER_MINUTE

from tests.conftest import OVERHEAD

from tests.test_request import MAX_PAGES

# pylint: disable=redefined-outer-name

@pytest.fixture
def send_max_minute(client: TestClient, example_url: str, path_url: str):
    """Send the limit of messages that can be sent in one minute."""

    def send():
        real_content = requests.get(example_url.format(MAX_PAGES))

        for _ in range(MAX_REQUESTS_PER_MINUTE):
            proxy_content = client.get(path_url.format(MAX_PAGES))
            assert proxy_content.content == real_content.content

    return send


def test_minute_limit(send_max_minute: Callable, client: TestClient, path_url: str):
    """Test that after message limit is reached the user is blocked."""
    send_max_minute()
    blocked_content = client.get(path_url.format(MAX_PAGES))
    assert blocked_content.status_code == status.HTTP_429_TOO_MANY_REQUESTS


def test_unblocking(
    send_max_minute: Callable, client: TestClient, path_url: str
):
    """Test that after a minute passes the user is not blocked."""
    send_max_minute()
    blocked_content = client.get(path_url.format(MAX_PAGES))
    assert blocked_content.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    time.sleep(60)  # Wait to the end of the block

    proxy_content = client.get(path_url.format(MAX_PAGES))
    assert proxy_content.status_code == status.HTTP_200_OK


def test_day_limit(
    send_max_minute: Callable,
    client: TestClient,
    path_url: str,
    example_url: str,
    mock_limiter,
):
    """Test that by-minute blocking and by-day blocking co-exist."""
    app.state.limiter = mock_limiter
    send_max_minute()
    time.sleep(60)  # One minute.
    real_content = requests.get(example_url.format(MAX_PAGES))

    for _ in range(OVERHEAD):
        proxy_content = client.get(path_url.format(MAX_PAGES))
        assert proxy_content.content == real_content.content

    blocked_content = client.get(path_url.format(MAX_PAGES))
    assert blocked_content.status_code == status.HTTP_429_TOO_MANY_REQUESTS
