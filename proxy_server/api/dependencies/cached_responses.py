"""Caching management and access."""
from functools import lru_cache
from typing import Dict, Annotated

from fastapi import Depends
from pydantic import AnyUrl
from cachetools import TTLCache
from aiohttp import ClientResponse

from proxy_server.api.dependencies.request_parsing import get_full_path

MAX_REQUESTS_PER_DAY = 1000
DAY_CACHE_IN_SECONDS = 60 * 60 * 24


@lru_cache
def responses_cache() -> TTLCache:
    """Create requests path and responses cache."""
    return TTLCache(MAX_REQUESTS_PER_DAY, ttl=DAY_CACHE_IN_SECONDS)


async def get_cached_response(
    path: Annotated[AnyUrl, Depends(get_full_path)],
    cached_responses: Annotated[Dict[str, ClientResponse], Depends(responses_cache)],
) -> ClientResponse:
    """Get cached response by path."""
    response = cached_responses.get(path.unicode_string())
    return response
