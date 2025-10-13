from cachelib import SimpleCache
import redis

def get_cache_client():
    try:
        # Try Redis first
        return redis.Redis(host='localhost', port=6379, db=0)
    except Exception:
        # Fallback to in-memory cache
        return SimpleCache()
