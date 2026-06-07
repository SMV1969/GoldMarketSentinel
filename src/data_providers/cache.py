import time

_cache = {}

def get_cached(key, ttl=60):
    if key in _cache:
        value, timestamp = _cache[key]
        if time.time() - timestamp < ttl:
            return value
    return None


def set_cache(key, value):
    _cache[key] = (value, time.time())
