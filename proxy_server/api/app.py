"""App for proxy server."""
from fastapi import FastAPI

from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler, Limiter

from proxy_server.api.routes.proxy import router
from proxy_server.api.dependencies.cached_responses import MAX_REQUESTS_PER_DAY

MAX_REQUESTS_PER_MINUTE = 10

LIMITS = [f"{MAX_REQUESTS_PER_MINUTE}/minute", f"{MAX_REQUESTS_PER_DAY}/day"]

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=LIMITS,
)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.include_router(router)
