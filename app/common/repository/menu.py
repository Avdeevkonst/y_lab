import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
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
        menus = await self.session.query(self.model).all()
        list_menu_responses = []
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
            menu_response = GetAllMenu(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count,
            )
            list_menu_responses.append(menu_response)
        return list_menu_responses

    async def get(self, target_menu_id: uuid.UUID) -> GetAllMenu:
        menu = (
            await self.session.query(self.model)
            .filter(self.model.id == target_menu_id)
            .first()
        )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        submenus_count = (
            await self.session.query(Submenu)
            .filter(Submenu.menu_id == target_menu_id)
            .count()
        )
        dishes_count = (
            await self.session.query(Dish)
            .join(Submenu)
            .filter(Submenu.menu_id == target_menu_id)
            .count()
        )
        return GetAllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
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
        stmt = select(self.model).where(self.model.id == target_menu_id)
        result = await self.session.execute(stmt)
        menu = result.scalars().first()
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

        # if not menu:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="menu not found",
        #     )
        #
        # menu.title = menu_data.title
        # menu.description = menu_data.description
        # await self.session.commit()
        # await self.session.refresh(menu)
        # return menu

    async def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        menu = (
            await self.session.query(self.model)
            .filter(self.model.id == target_menu_id)
            .first()
        )

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
