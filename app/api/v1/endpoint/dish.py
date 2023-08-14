import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status

from app.common.services.dish import DishService
from app.schemas import CreateDishSchema, DishResponse, UpdateDishSchema

router = APIRouter()


@router.get(
    "/",
    response_model=list[DishResponse],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список блюд",
)
async def get_all_dishes_handler(
        target_submenu_id: uuid.UUID,
        dish: Annotated[DishService, Depends()],
):
    return await dish.get_all(target_submenu_id)


@router.get(
    "/{target_dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает определённое блюдо",
)
async def get_dish_handler(
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish: Annotated[DishService, Depends()],
):
    return await dish.get(target_menu_id, target_submenu_id, target_dish_id)


@router.post(
    "/",
    response_model=DishResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создаёт блюдо",
)
async def create_dish_handler(
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        dish_data: CreateDishSchema,
        dish: Annotated[DishService, Depends()],
        background_tasks: BackgroundTasks,
):
    return await dish.create(target_menu_id, target_submenu_id, dish_data, background_tasks)


@router.patch(
    "/{target_dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновляет блюдо",
)
async def update_dish_handler(
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish_data: Annotated[UpdateDishSchema, Body(...)],
        dish: Annotated[DishService, Depends()],
        background_tasks: BackgroundTasks,
):
    return await dish.update(
        target_menu_id, target_submenu_id, target_dish_id, dish_data, background_tasks
    )


@router.delete(
    "/{target_dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаляет блюдо",
)
async def delete_dish_handler(
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish: Annotated[DishService, Depends()],
        background_tasks: BackgroundTasks,
):
    return await dish.delete(target_menu_id, target_submenu_id, target_dish_id, background_tasks)
