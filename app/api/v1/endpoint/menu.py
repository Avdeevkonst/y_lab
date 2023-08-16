import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from starlette.responses import JSONResponse

from app.common.services.menu import MenuService
from app.db.models import Menu
from app.schemas import (
    CreateMenuSchema,
    GetAllMenu,
    MenuBaseSchema,
    MenuResponse,
    UpdateMenuSchema,
)

router = APIRouter()


# Возвращает все меню
@router.get("/", response_model=list[MenuResponse])
async def get_all_menus(
    menu: Annotated[MenuService, Depends()],
) -> list[MenuBaseSchema]:
    return await menu.get_all()


# Возвращает меню
@router.get("/{target_menu_id}", response_model=GetAllMenu)
async def get_menu(target_menu_id: uuid.UUID, menu: Annotated[MenuService, Depends()]):
    return await menu.get(target_menu_id)


# Создаёт меню
@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: CreateMenuSchema,
    menu: Annotated[MenuService, Depends()],
    background_tasks: BackgroundTasks,
):
    return await menu.create(menu_data, background_tasks)


# Обновляет меню
@router.patch("/{target_menu_id}", response_model=MenuResponse)
async def update_menu(
    target_menu_id: uuid.UUID,
    menu_data: Annotated[UpdateMenuSchema, Body(...)],
    menu: Annotated[MenuService, Depends()],
    background_tasks: BackgroundTasks,
) -> type[Menu]:
    return await menu.update(target_menu_id, menu_data, background_tasks)


# Удаляет меню
@router.delete("/{target_menu_id}", status_code=status.HTTP_200_OK)
async def delete_menu(
    target_menu_id: uuid.UUID,
    menu: Annotated[MenuService, Depends()],
    background_tasks: BackgroundTasks,
) -> JSONResponse:
    return await menu.delete(target_menu_id, background_tasks)
