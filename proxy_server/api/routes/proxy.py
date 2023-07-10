"""Proxy server route."""
from typing import Annotated, Union, Dict

from pydantic import AnyUrl
from fastapi.responses import Response
from fastapi import APIRouter, Depends, Request
from aiohttp import ClientResponse, ClientSession


from proxy_server.api.dependencies.chached_responses import (
    get_cached_response,
    responses_cache,
)
from proxy_server.api.dependencies.request_parsing import parsed_headers


router = APIRouter(tags=["proxy"])


@router.get("/{path:path}")
async def proxy(
    path: AnyUrl,
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
        text_content = await cached_response.text()
        response = cached_response

    else:
        async with ClientSession(headers=headers) as session:
            async with session.request(
                method=request.method,
                url=path.unicode_string(),
                data=await request.body(),
            ) as response:
                text_content = await response.text()
            cache.update({path.unicode_string(): response})

    return Response(
        content=text_content,
        status_code=response.status,
        media_type=response.content_type,
    )
