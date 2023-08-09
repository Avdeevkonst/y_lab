import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.db.database import get_db
from app.db.models import Dish, Menu, Submenu
from app.schemas import CreateDishSchema, DishBaseSchema


class DishRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]):
        self.session: Session = session
        self.model = Dish

    # Возвращает все блюда для определенного подменю
    def get_all(self, target_submenu_id: uuid.UUID) -> list[type[Dish]]:
        return (
            self.session.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()
        )

    # Создаёт блюдо для указанного подменю
    def create(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        dish_data: CreateDishSchema,
    ) -> Dish:
        # Проверяем, существуют ли указанные меню и подменю
        menu = self.session.query(Menu).filter(Menu.id == target_menu_id).first()
        submenu = (
            self.session.query(Submenu)
            .filter(Submenu.id == target_submenu_id, Submenu.menu_id == target_menu_id)
            .first()
        )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        # Создаем новое блюдо
        new_dish = Dish(**dish_data.model_dump(), submenu_id=target_submenu_id)
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    # Возвращает блюдо по ero ID и принадлежности к указанному меню и подменю
    def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> Dish:
        dish = self.search_dish(target_menu_id, target_submenu_id, target_dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        return dish

    # Обновляет блюдо по ero ID и принадлежности к указанному меню и подменю
    def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish_data: DishBaseSchema,
    ) -> Submenu:
        dish = self.search_dish(target_menu_id, target_submenu_id, target_dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        for field, value in dish_data.model_dump().items():
            setattr(dish, field, value)

        self.session.commit()
        self.session.refresh(dish)
        return dish

    # Удаляет блюдо по ero ID и принадлежности к указанному меню и подменю
    def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> JSONResponse:
        dish = self.search_dish(target_menu_id, target_submenu_id, target_dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        self.session.delete(dish)
        self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Dish {dish.title} deleted successfully"},
        )

    def search_dish(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ):
        return (
            self.session.query(Dish)
            .join(Submenu, Submenu.id == Dish.submenu_id)
            .filter(Submenu.menu_id == target_menu_id)
            .filter(Dish.submenu_id == target_submenu_id)
            .filter(Dish.id == target_dish_id)
            .first()
        )
