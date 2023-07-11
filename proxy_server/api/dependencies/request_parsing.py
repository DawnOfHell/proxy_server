"""All functionalities to be preformed on requests objects."""
from typing import Annotated

from pydantic import AnyUrl
from fastapi import Request, Depends
from starlette.datastructures import MutableHeaders


async def get_full_path(request: Request):
    """Get full path of proxied path."""
    base_url = str(request.base_url)
    path_url = str(request.url).replace(base_url, "")
    return AnyUrl(path_url)


async def parsed_headers(
    request: Request, path: Annotated[AnyUrl, Depends(get_full_path)]
) -> MutableHeaders:
    """Get and modify headers from request."""
    modified_headers = request.headers.mutablecopy()
    remote_hostname = path.host or ""
    remote_hostname += f":{path.port}" if path.port else ""
    modified_headers["host"] = remote_hostname
    modified_headers["scheme"] = path.scheme
    return modified_headers
