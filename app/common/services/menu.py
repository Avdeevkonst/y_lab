import uuid
from typing import Annotated

from fastapi import BackgroundTasks, Depends
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

    async def create(
        self, menu: CreateMenuSchema, background_tasks: BackgroundTasks,
    ) -> Menu:
        item = await self.repository.create(menu)
        background_tasks.add_task(self.cache.invalidate("all_menus", "all_data"))
        return item

    async def update(
        self,
        target_menu_id: uuid.UUID,
        menu_data: UpdateMenuSchema,
        background_tasks: BackgroundTasks,
    ) -> type[Menu]:
        item = await self.repository.update(target_menu_id, menu_data)
        background_tasks.add_task(
            self.cache.invalidate("all_menus", f"menu_{target_menu_id}", "all_data"),
        )
        return item

    async def delete(
        self, target_menu_id: uuid.UUID, background_tasks: BackgroundTasks,
    ) -> JSONResponse:
        item = await self.repository.delete(target_menu_id)
        background_tasks.add_task(
            self.cache.invalidate("all_menus", f"menu_{target_menu_id}", "all_data"),
        )
        return item
