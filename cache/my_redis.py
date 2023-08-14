import json
import os
from typing import Any

import aioredis
from fastapi.encoders import jsonable_encoder


class Cache:
    def __init__(self, redis_host: str):
        self.redis_client = aioredis.StrictRedis(host=redis_host, port=6379, db=0)

    async def get(self, key: str):
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return cached_data.decode("utf-8")
        return None

    async def set(self, key: str, value: Any):
        await self.redis_client.set(key, value)

    async def cached_or_fetch(
        self,
        cache_key: str,
        repository_function: Any,
        *args: Any,
        **kwargs: Any,
    ):
        cached_result = await self.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        items = await repository_function(*args, **kwargs)
        json_compatible_value = jsonable_encoder(items)
        await self.set(cache_key, json.dumps(json_compatible_value))
        return items

    async def invalidate(self, *args: str):
        for cache_key in args:
            await self.redis_client.delete(cache_key)


REDIS_HOST: str = str(os.getenv("REDIS_HOST"))
isinstance_cache = Cache(REDIS_HOST)
