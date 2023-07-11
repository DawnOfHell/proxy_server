"""Proxy server route."""
from typing import Annotated, Union, Dict

from pydantic import AnyUrl
from fastapi.responses import Response
from fastapi import APIRouter, Depends, Request
from aiohttp import ClientResponse, ClientSession


from proxy_server.api.dependencies.cached_responses import (
    get_cached_response,
    responses_cache,
)
from proxy_server.api.dependencies.request_parsing import parsed_headers, get_full_path


router = APIRouter(tags=["proxy"])


@router.get("/{path:path}")
async def proxy(
    url: Annotated[AnyUrl, Depends(get_full_path)],
    request: Request,
    headers: Annotated[dict, Depends(parsed_headers)],
    cached_response: Annotated[
        Union[ClientResponse, None], Depends(get_cached_response)
    ],
    cache: Annotated[Dict[str, ClientResponse], Depends(responses_cache)],
):
    """Get specified path in an async way, if response already exists in cache
    return it instead"""
    if cached_response:
        response = cached_response

    else:
        async with ClientSession(headers=headers) as session:
            async with session.request(
                method=request.method,
                url=url.unicode_string(),
                data=await request.body(),
            ) as response:
                content = await response.content.read()
                response = Response(
                    content=content,
                    status_code=response.status,
                    media_type=response.content_type,
                )
            cache.update({url.unicode_string(): response})

    return response
