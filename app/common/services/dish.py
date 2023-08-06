import uuid
from typing import Annotated

from fastapi import Depends
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

    def get_all(self, target_submenu_id: uuid.UUID) -> list[type[Dish]]:
        return self.cache.cached_or_fetch(
            "all_dishes",
            self.repository.get_all,
            target_submenu_id,
        )

    def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> Submenu:
        return self.cache.cached_or_fetch(
            f"dish_{target_dish_id}",
            self.repository.get,
            target_menu_id,
            target_submenu_id,
            target_dish_id,
        )

    def create(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        dish_data: CreateDishSchema,
    ) -> Dish:
        item = self.repository.create(target_menu_id, target_submenu_id, dish_data)
        self.cache.invalidate("all_dishes")
        return item

    def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish_data: UpdateDishSchema,
    ) -> Submenu:
        item = self.repository.update(
            target_menu_id,
            target_submenu_id,
            target_dish_id,
            dish_data,
        )
        self.cache.invalidate("all_dishes", f"dish_{target_dish_id}")
        return item

    def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> JSONResponse:
        item = self.repository.delete(target_menu_id, target_submenu_id, target_dish_id)
        self.cache.invalidate(
            "all_dishes",
            "all_submenus",
            "all_menus",
            f"dish_{target_dish_id}",
            f"menu_{target_menu_id}",
            f"submenu_{target_submenu_id}",
        )
        return item
