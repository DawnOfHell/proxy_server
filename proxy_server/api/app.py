"""App for proxy server."""
from fastapi import FastAPI

from proxy_server.api.routes.proxy import router

app = FastAPI()
app.include_router(router)
