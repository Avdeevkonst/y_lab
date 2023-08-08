import uuid

from fastapi import APIRouter, Body, Depends, status

from app.common.services.dish import DishService
from app.schemas import CreateDishSchema, DishResponse, UpdateDishSchema

router = APIRouter()


@router.get(
    "/",
    response_model=list[DishResponse],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список блюд",
)
def get_all_dishes_handler(target_submenu_id: uuid.UUID, dish: DishService = Depends()):
    return dish.get_all(target_submenu_id)


@router.get(
    "/{target_dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает определённое блюдо",
)
def get_dish_handler(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    target_dish_id: uuid.UUID,
    dish: DishService = Depends(),
):
    return dish.get(target_menu_id, target_submenu_id, target_dish_id)


@router.post(
    "/",
    response_model=DishResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создаёт блюдо",
)
def create_dish_handler(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    dish_data: CreateDishSchema,
    dish: DishService = Depends(),
):
    return dish.create(target_menu_id, target_submenu_id, dish_data)


@router.patch(
    "/{target_dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновляет блюдо",
)
def update_dish_handler(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    target_dish_id: uuid.UUID,
    dish_data: UpdateDishSchema = Body(...),
    dish: DishService = Depends(),
):
    return dish.update(target_menu_id, target_submenu_id, target_dish_id, dish_data)


@router.delete(
    "/{target_dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаляет блюдо",
)
def delete_dish_handler(
    target_menu_id: uuid.UUID,
    target_submenu_id: uuid.UUID,
    target_dish_id: uuid.UUID,
    dish: DishService = Depends(),
):
    return dish.delete(target_menu_id, target_submenu_id, target_dish_id)
