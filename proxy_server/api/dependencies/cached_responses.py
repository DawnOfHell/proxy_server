"""Caching management and access."""
from functools import lru_cache
from cachetools import TTLCache


MAX_REQUESTS_PER_DAY = 1000
DAY_CACHE_IN_SECONDS = 60 * 60 * 24


# In fastapi in order to allow access to persistent objects,
# such as settings, in memory data stores and so on, we wrap the
# dependency with lru_cache.
@lru_cache
def responses_cache() -> TTLCache:
    """Create requests path and responses cache."""
    return TTLCache(MAX_REQUESTS_PER_DAY, ttl=DAY_CACHE_IN_SECONDS)
