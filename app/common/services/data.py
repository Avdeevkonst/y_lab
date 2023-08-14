from typing import Annotated

from fastapi import Depends

from app.common.repository.data import DataRepository
from cache.my_redis import isinstance_cache


class DataService:
    def __init__(self, repository: Annotated[DataRepository, Depends()]):
        self.repository = repository
        self.cache = isinstance_cache

    async def get_all(self):
        return await self.cache.cached_or_fetch("all_data", self.repository.get_all)
