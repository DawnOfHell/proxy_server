"""All functionalities to be preformed on requests objects."""
from urllib.parse import urlparse

from fastapi import Request
from starlette.datastructures import MutableHeaders

TRAILING_BACKSLASH = 1


async def parsed_headers(request: Request) -> MutableHeaders:
    """Get and modify headers from request."""
    schema_and_host = urlparse(request.url.path[TRAILING_BACKSLASH:])
    modified_headers = request.headers.mutablecopy()
    remote_hostname = schema_and_host.hostname or ""
    remote_hostname += f":{schema_and_host.port}" if schema_and_host.port else ""
    modified_headers["host"] = remote_hostname
    modified_headers["scheme"] = schema_and_host.scheme
    return modified_headers


async def get_full_url(request: Request) -> str:
    """Get full path including query params."""
    return f"{request.url.path[TRAILING_BACKSLASH:]}?{request.url.query}"
