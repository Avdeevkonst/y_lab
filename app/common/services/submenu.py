import uuid
from typing import Annotated

from fastapi import BackgroundTasks, Depends
from starlette.responses import JSONResponse

from app.common.repository.submenu import SubMenuRepository
from app.db.models import Submenu
from app.schemas import (
    CreateSubmenuSchema,
    FilteredSubmenuResponse,
    SubmenuResponse,
    UpdateSubmenuSchema,
)
from cache.my_redis import isinstance_cache


class SubMenuService:
    def __init__(self, repository: Annotated[SubMenuRepository, Depends()]):
        self.repository = repository
        self.cache = isinstance_cache

    async def get_all(self, target_menu_id: uuid.UUID) -> list[SubmenuResponse]:
        return await self.cache.cached_or_fetch(
            "all_submenus",
            self.repository.get_all,
            target_menu_id,
        )

    async def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
    ) -> FilteredSubmenuResponse:
        return await self.cache.cached_or_fetch(
            f"submenu_{target_submenu_id}",
            self.repository.get,
            target_menu_id,
            target_submenu_id,
        )

    async def create(
        self,
        target_menu_id: uuid.UUID,
        submenu: CreateSubmenuSchema,
        background_tasks: BackgroundTasks,
    ) -> Submenu:
        background_tasks.add_task(
            self.cache.invalidate(
                f"menu_{target_menu_id}",
                "all_submenus",
                "all_menus",
                "all_data",
            ),
        )
        return await self.repository.create(target_menu_id, submenu)

    async def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        submenu_data: UpdateSubmenuSchema,
        background_tasks: BackgroundTasks,
    ) -> type[Submenu]:
        item = await self.repository.update(
            target_menu_id, target_submenu_id, submenu_data,
        )
        background_tasks.add_task(
            self.cache.invalidate(
                "all_submenus", f"submenu_{target_submenu_id}", "all_data",
            ),
        )
        return item

    async def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        background_tasks: BackgroundTasks,
    ) -> JSONResponse:
        item = await self.repository.delete(target_menu_id, target_submenu_id)
        background_tasks.add_task(
            self.cache.invalidate(
                "all_submenus",
                "all_menus",
                f"submenu_{target_submenu_id}",
                f"menu_{target_menu_id}",
                "all_data",
            ),
        )
        return item
