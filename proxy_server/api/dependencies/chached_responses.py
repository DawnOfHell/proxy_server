"""Caching management and access."""
from typing import Dict, Annotated
from aiohttp import ClientResponse
from cachetools.func import ttl_cache

from fastapi import Depends

from proxy_server.api.dependencies.request_parsing import get_full_url

DAY_CACHE_IN_SECONDS = 60 * 60 * 24


@ttl_cache(ttl=DAY_CACHE_IN_SECONDS)
def responses_cache() -> Dict[str, ClientResponse]:
    """Create requests path and responses cache."""
    return {}


async def get_cached_response(
    full_path: Annotated[str, Depends(get_full_url)],
    cached_responses: Annotated[Dict[str, ClientResponse],
    Depends(responses_cache)]) -> ClientResponse:
    """Get cached response by path."""
    response = cached_responses.get(full_path)
    return response
