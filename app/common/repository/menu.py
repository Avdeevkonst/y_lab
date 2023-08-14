import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.db.database import get_db
from app.db.models import Dish, Menu, Submenu
from app.schemas import CreateMenuSchema, GetAllMenu, UpdateMenuSchema


class MenuRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]):
        self.session: Session = session
        self.model = Menu

    # Функция для подсчета количества подменю и блюд, и выдачи списка меню
    async def get_all(self) -> list[GetAllMenu]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        menus = result.scalars().fetchall()
        list_menu_responses = []
        for menu in menus:
            submenus_query = select(func.count(Submenu.id)).filter(
                Submenu.menu_id == menu.id,
            )
            dishes_query = (
                select(func.count(Dish.id))
                .join(Submenu)
                .filter(Submenu.menu_id == menu.id)
            )
            submenus_count = await self.session.execute(submenus_query)
            dishes_count = await self.session.execute(dishes_query)
            submenus_result = len(submenus_count.all())
            dishes_result = len(dishes_count.all())
            menu_response = GetAllMenu(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_result,
                dishes_count=dishes_result,
            )
            list_menu_responses.append(menu_response)
        return list_menu_responses

    async def get(self, target_menu_id: uuid.UUID) -> GetAllMenu:
        menu = await self.search_menu(target_menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        submenus_query = select(func.count(Submenu.id)).filter(
            Submenu.menu_id == menu.id,
        )
        dishes_query = (
            select(func.count(Dish.id)).join(Submenu).filter(Submenu.menu_id == menu.id)
        )
        submenus_count = await self.session.execute(submenus_query)
        dishes_count = await self.session.execute(dishes_query)
        submenus_result = len(submenus_count.all())
        dishes_result = len(dishes_count.all())
        return GetAllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_result,
            dishes_count=dishes_result,
        )

    async def create(self, menu: CreateMenuSchema) -> Menu:
        new_menu = self.model(**menu.model_dump())
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        return new_menu

    async def update(
        self,
        target_menu_id: uuid.UUID,
        menu_data: UpdateMenuSchema,
    ) -> type[Menu]:
        menu = await self.search_menu(target_menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        menu.title = menu_data.title
        menu.description = menu_data.description
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        menu = await self.search_menu(target_menu_id)

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        menu_title = menu.title
        await self.session.delete(menu)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Menu {menu_title} deleted successfully"},
        )

    async def search_menu(self, target_menu_id: uuid.UUID):
        stmt = select(self.model).where(self.model.id == target_menu_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
