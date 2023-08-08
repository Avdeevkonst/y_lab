import uuid
from typing import Annotated

from fastapi import Depends
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

    def get_all(self, target_menu_id: uuid.UUID) -> list[SubmenuResponse]:
        return self.cache.cached_or_fetch(
            "all_submenus",
            self.repository.get_all,
            target_menu_id,
        )

    def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
    ) -> FilteredSubmenuResponse:
        return self.cache.cached_or_fetch(
            f"submenu_{target_submenu_id}",
            self.repository.get,
            target_menu_id,
            target_submenu_id,
        )

    def create(
        self,
        target_menu_id: uuid.UUID,
        submenu: CreateSubmenuSchema,
    ) -> Submenu:
        self.cache.invalidate("all_submenus")
        return self.repository.create(target_menu_id, submenu)

    def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        submenu_data: UpdateSubmenuSchema,
    ) -> type[Submenu]:
        item = self.repository.update(target_menu_id, target_submenu_id, submenu_data)
        self.cache.invalidate("all_submenus", f"submenu_{target_submenu_id}")
        return item

    def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
    ) -> JSONResponse:
        item = self.repository.delete(target_menu_id, target_submenu_id)
        self.cache.invalidate(
            "all_submenus",
            "all_menus",
            f"submenu_{target_submenu_id}",
            f"menu_{target_menu_id}",
        )
        return item
