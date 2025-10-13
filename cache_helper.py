# cache_helper.py
"""
Return a cache object. If REDIS_URL env is set and Redis is reachable,
use Redis. Otherwise fall back to cachelib.SimpleCache.
The Redis client used stores JSON strings; we wrap get/set accordingly.
"""
import os
import json
from cachelib import SimpleCache

REDIS_URL = os.environ.get("REDIS_URL")  # on Render you can set this if you have Redis

def get_cache_client():
    # Try Redis if REDIS_URL is set
    try:
        if REDIS_URL:
            import redis
            r = redis.from_url(REDIS_URL, decode_responses=True)
            # quick ping test
            r.ping()
            return RedisWrapper(r)
    except Exception:
        pass
    # fallback
    return SimpleCacheWrapper(SimpleCache())

class SimpleCacheWrapper:
    def __init__(self, cache):
        self.cache = cache
    def get(self, key):
        return self.cache.get(key)
    def set(self, key, value, timeout=300):
        return self.cache.set(key, value, timeout)
    def delete(self, key):
        return self.cache.delete(key)

class RedisWrapper:
    def __init__(self, rclient):
        self.r = rclient
    def get(self, key):
        v = self.r.get(key)
        if v is None:
            return None
        try:
            return json.loads(v)
        except Exception:
            return v
    def set(self, key, value, timeout=300):
        try:
            self.r.setex(key, timeout, json.dumps(value))
            return True
        except Exception:
            return False
    def delete(self, key):
        return self.r.delete(key)
