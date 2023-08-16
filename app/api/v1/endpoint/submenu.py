import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status

from app.common.services.submenu import SubMenuService
from app.schemas import (
    CreateSubmenuSchema,
    FilteredSubmenuResponse,
    SubmenuResponse,
    UpdateSubmenuSchema,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[SubmenuResponse],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список подменю",
)
async def get_submenus(
    target_menu_id: uuid.UUID,
    submenu: Annotated[SubMenuService, Depends()],
):
    return await submenu.get_all(target_menu_id)


@router.get(
    "/{target_submenu_id}",
    response_model=FilteredSubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает определённое подменю",
)
async def get_submenu(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    submenu: Annotated[SubMenuService, Depends()],
):
    return await submenu.get(target_menu_id, target_submenu_id)


@router.post(
    "/",
    response_model=SubmenuResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создаёт подменю",
)
async def create_submenu(
    target_menu_id: uuid.UUID,
    submenu_data: CreateSubmenuSchema,
    submenu: Annotated[SubMenuService, Depends()],
    background_tasks: BackgroundTasks,
):
    return await submenu.create(target_menu_id, submenu_data, background_tasks)


@router.patch(
    "/{target_submenu_id}",
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновляет подменю",
)
async def update_submenu(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    submenu_data: Annotated[UpdateSubmenuSchema, Body(...)],
    submenu: Annotated[SubMenuService, Depends()],
    background_tasks: BackgroundTasks,
):
    return await submenu.update(
        target_menu_id,
        target_submenu_id,
        submenu_data,
        background_tasks,
    )


@router.delete(
    "/{target_submenu_id}",
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаляет подменю",
)
async def delete_submenu(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    submenu: Annotated[SubMenuService, Depends()],
    background_tasks: BackgroundTasks,
):
    return await submenu.delete(target_menu_id, target_submenu_id, background_tasks)
