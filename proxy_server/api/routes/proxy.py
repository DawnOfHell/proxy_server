"""Proxy server route."""
from typing import Annotated, Union, Dict

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from aiohttp import ClientResponse, ClientSession

from proxy_server.api.dependencies.chached_responses import (
    get_cached_response,
    responses_cache,
)
from proxy_server.api.dependencies.request_parsing import parsed_headers, get_full_url


router = APIRouter(tags=["proxy"])


@router.get("/{path:path}")
async def proxy(
    headers: Annotated[dict, Depends(parsed_headers)],
    full_path: Annotated[str, Depends(get_full_url)],
    cached_response: Annotated[Union[ClientResponse, None], Depends(get_cached_response)],
    responses_cache: Annotated[Dict[str, ClientResponse], Depends(responses_cache)]):
    """Get specified path in an async way, if response already exists in cache
     return it instead"""
    if cached_response:
        response_text = await cached_response.text()
        return HTMLResponse(content=response_text,
                            status_code=cached_response.status)

    async with ClientSession(headers=headers) as session:
        async with session.get(full_path) as response:
            text_content = await response.text()
        responses_cache.update({full_path: response})
    return HTMLResponse(content=text_content, status_code=response.status)
