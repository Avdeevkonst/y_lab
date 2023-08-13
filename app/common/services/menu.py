import uuid
from typing import Annotated

from fastapi import Depends
from starlette.responses import JSONResponse

from app.common.repository.menu import MenuRepository
from app.db.models import Menu
from app.schemas import CreateMenuSchema, GetAllMenu, UpdateMenuSchema
from cache.my_redis import isinstance_cache


class MenuService:
    def __init__(self, repository: Annotated[MenuRepository, Depends()]):
        self.repository = repository
        self.cache = isinstance_cache

    async def get_all(self) -> list[GetAllMenu]:
        return await self.cache.cached_or_fetch("all_menus", self.repository.get_all)

    async def get(self, target_menu_id: uuid.UUID) -> GetAllMenu:
        return await self.cache.cached_or_fetch(
            f"menu_{target_menu_id}",
            self.repository.get,
            target_menu_id,
        )

    async def create(self, menu: CreateMenuSchema) -> Menu:
        item = await self.repository.create(menu)
        await self.cache.invalidate("all_menus")
        return item

    async def update(
        self,
        target_menu_id: uuid.UUID,
        menu_data: UpdateMenuSchema,
    ) -> type[Menu]:
        item = await self.repository.update(target_menu_id, menu_data)
        await self.cache.invalidate("all_menus", f"menu_{target_menu_id}")
        return item

    async def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        item = await self.repository.delete(target_menu_id)
        await self.cache.invalidate("all_menus", f"menu_{target_menu_id}")
        return item
