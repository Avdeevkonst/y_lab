import json

import redis
from fastapi.encoders import jsonable_encoder


class Cache:
    def __init__(self, redis_host: str):
        self.redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)

    def get(self, key):
        cached_data = self.redis_client.get(key)
        if cached_data:
            return cached_data.decode("utf-8")
        return None

    def set(self, key, value):
        self.redis_client.set(key, value)

    def cached_or_fetch(self, cache_key: str, repository_function, *args, **kwargs):
        cached_result = self.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        items = repository_function(*args, **kwargs)
        json_compatible_value = jsonable_encoder(items)
        self.set(cache_key, json.dumps(json_compatible_value))
        return items

    def invalidate(self, *args: str):
        for cache_key in args:
            self.redis_client.delete(cache_key)


isinstance_cache = Cache("localhost")
