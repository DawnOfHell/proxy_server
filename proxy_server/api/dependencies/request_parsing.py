"""All functionalities to be preformed on requests objects."""
from pydantic import AnyUrl
from fastapi import Request
from starlette.datastructures import MutableHeaders


async def parsed_headers(request: Request, path: AnyUrl) -> MutableHeaders:
    """Get and modify headers from request."""
    modified_headers = request.headers.mutablecopy()
    remote_hostname = path.host or ""
    remote_hostname += f":{path.port}" if path.port else ""
    modified_headers["host"] = remote_hostname
    modified_headers["scheme"] = path.scheme
    return modified_headers
