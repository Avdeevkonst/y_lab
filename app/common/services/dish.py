import uuid
from typing import Annotated

from fastapi import BackgroundTasks, Depends
from starlette.responses import JSONResponse

from app.common.repository.dish import DishRepository
from app.db.models import Dish, Submenu
from app.schemas import CreateDishSchema, UpdateDishSchema
from cache.my_redis import isinstance_cache


class DishCache:
    # методы кеширования
    pass


class DishService:
    def __init__(self, repository: Annotated[DishRepository, Depends()]):
        self.repository = repository
        self.cache = isinstance_cache

    async def get_all(self, target_submenu_id: uuid.UUID) -> list[type[Dish]]:
        return await self.cache.cached_or_fetch(
            "all_dishes",
            self.repository.get_all,
            target_submenu_id,
        )

    async def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> Submenu:
        return await self.cache.cached_or_fetch(
            f"dish_{target_dish_id}",
            self.repository.get,
            target_menu_id,
            target_submenu_id,
            target_dish_id,
        )

    async def create(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        dish_data: CreateDishSchema,
        background_tasks: BackgroundTasks,
    ) -> Dish:
        item = await self.repository.create(
            target_menu_id, target_submenu_id, dish_data,
        )
        background_tasks.add_task(
            self.cache.invalidate(
                "all_dishes",
                f"menu_{target_menu_id}",
                f"submenu_{target_submenu_id}",
                "all_menus",
                "all_submenus",
                "all_data",
            ),
        )

        return item

    async def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish_data: UpdateDishSchema,
        background_tasks: BackgroundTasks,
    ) -> Submenu:
        item = await self.repository.update(
            target_menu_id,
            target_submenu_id,
            target_dish_id,
            dish_data,
        )
        background_tasks.add_task(
            self.cache.invalidate("all_dishes", f"dish_{target_dish_id}", "all_data"),
        )
        return item

    async def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        background_tasks: BackgroundTasks,
    ) -> JSONResponse:
        item = await self.repository.delete(
            target_menu_id, target_submenu_id, target_dish_id,
        )
        background_tasks.add_task(
            self.cache.invalidate(
                "all_dishes",
                "all_submenus",
                "all_menus",
                f"dish_{target_dish_id}",
                f"menu_{target_menu_id}",
                f"submenu_{target_submenu_id}",
                "all_data",
            ),
        )
        return item
