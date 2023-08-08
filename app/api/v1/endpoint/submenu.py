import uuid

from fastapi import APIRouter, Body, Depends, status

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
def get_submenus(target_menu_id: uuid.UUID, submenu: SubMenuService = Depends()):
    return submenu.get_all(target_menu_id)


@router.get(
    "/{target_submenu_id}",
    response_model=FilteredSubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает определённое подменю",
)
def get_submenu(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    submenu: SubMenuService = Depends(),
):
    return submenu.get(target_menu_id, target_submenu_id)


@router.post(
    "/",
    response_model=SubmenuResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создаёт подменю",
)
def create_submenu(
    target_menu_id: uuid.UUID,
    submenu_data: CreateSubmenuSchema,
    submenu: SubMenuService = Depends(),
):
    return submenu.create(target_menu_id, submenu_data)


@router.patch(
    "/{target_submenu_id}",
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновляет подменю",
)
def update_submenu(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    submenu_data: UpdateSubmenuSchema = Body(...),
    submenu: SubMenuService = Depends(),
):
    return submenu.update(target_menu_id, target_submenu_id, submenu_data)


@router.delete(
    "/{target_submenu_id}",
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаляет подменю",
)
def delete_submenu(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    submenu: SubMenuService = Depends(),
):
    return submenu.delete(target_menu_id, target_submenu_id)
