import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from app.common.services.menu import MenuService
from app.db.models import Menu
from app.schemas import CreateMenuSchema, MenuBaseSchema, MenuResponse, UpdateMenuSchema

router = APIRouter()


# Возвращает все меню
@router.get("/", response_model=list[MenuResponse])
def get_all_menus(menu: Annotated[MenuService, Depends()]) -> list[MenuBaseSchema]:
    return menu.get_all()


# Возвращает меню
@router.get("/{target_menu_id}", response_model=MenuResponse)
def get_menu(target_menu_id: uuid.UUID, menu: Annotated[MenuService, Depends()]):
    return menu.get(target_menu_id)


# Создаёт меню
@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(menu_data: CreateMenuSchema, menu: Annotated[MenuService, Depends()]):
    return menu.create(menu_data)


# Обновляет меню
@router.patch("/{target_menu_id}", response_model=MenuResponse)
def update_menu(
    target_menu_id: uuid.UUID,
    menu_data: Annotated[UpdateMenuSchema, Body(...)],
    menu: Annotated[MenuService, Depends()],
) -> type[Menu]:
    return menu.update(target_menu_id, menu_data)


# Удаляет меню
@router.delete("/{target_menu_id}", status_code=status.HTTP_200_OK)
def delete_menu(
    target_menu_id: uuid.UUID,
    menu: Annotated[MenuService, Depends()],
) -> JSONResponse:
    return menu.delete(target_menu_id)
