import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.db.database import get_db
from app.db.models import Dish, Menu, Submenu
from app.schemas import CreateMenuSchema, MenuResponse, UpdateMenuSchema


class MenuRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]):
        self.session: Session = session
        self.model = Menu

    # Функция для подсчета количества подменю и блюд, и выдачи списка меню
    def get_all(self) -> list[MenuResponse]:
        menus = self.session.query(self.model).all()
        menu_responses = []
        for menu in menus:
            submenus_count = (
                self.session.query(Submenu).filter(Submenu.menu_id == menu.id).count()
            )
            dishes_count = (
                self.session.query(Dish)
                .join(Submenu)
                .filter(Submenu.menu_id == menu.id)
                .count()
            )
            menu_response = MenuResponse(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count,
            )
            menu_responses.append(menu_response)
        return menu_responses

    def get(self, target_menu_id: uuid.UUID) -> MenuResponse:
        # Получаем меню по айди
        menu = (
            self.session.query(self.model)
            .filter(self.model.id == target_menu_id)
            .first()
        )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        # Подсчитываем количество подменю и блюд для данного меню
        submenus_count = (
            self.session.query(Submenu)
            .filter(Submenu.menu_id == target_menu_id)
            .count()
        )
        dishes_count = (
            self.session.query(Dish)
            .join(Submenu)
            .filter(Submenu.menu_id == target_menu_id)
            .count()
        )

        # Создаем экземпляр схемы AllMenu и заполняем поля
        return MenuResponse(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )

    def create(self, menu: CreateMenuSchema) -> Menu:
        new_menu = self.model(**menu.model_dump())
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def update(
        self,
        target_menu_id: uuid.UUID,
        menu_data: UpdateMenuSchema,
    ) -> type[Menu]:
        menu = (
            self.session.query(self.model)
            .filter(self.model.id == target_menu_id)
            .first()
        )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        menu.title = menu_data.title
        menu.description = menu_data.description
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        menu = (
            self.session.query(self.model)
            .filter(self.model.id == target_menu_id)
            .first()
        )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        menu_title = menu.title
        self.session.delete(menu)
        self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Menu {menu_title} deleted successfully"},
        )
