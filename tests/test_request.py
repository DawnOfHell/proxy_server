"""Test sending basic requests"""
import pytest
import requests
from fastapi.testclient import TestClient

MAX_PAGES = 2  # From the api entrypoint tested

PAGES_ITER = [None] + [*range(1, MAX_PAGES)]


@pytest.mark.parametrize("page_num", PAGES_ITER)
def test_request(client: TestClient, example_url: str, path_url: str, page_num: int):
    """Test that proxy work with and without query params."""
    real_content = requests.get(example_url.format(page_num))
    content_from_proxy = client.get(path_url.format(page_num))
    assert real_content.content == content_from_proxy.content
