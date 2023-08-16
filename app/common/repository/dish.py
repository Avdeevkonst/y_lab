import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
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

    async def get_all(self, target_submenu_id: uuid.UUID) -> list[type[Dish]]:
        stmt_dish = select(self.model).where(self.model.submenu_id == target_submenu_id)
        result_dish = await self.session.execute(stmt_dish)
        return result_dish.scalars().fetchall()

    async def create(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        dish_data: CreateDishSchema,
    ) -> Dish:
        stmt_dish = select(Menu).where(Menu.id == target_menu_id)
        result_dish = await self.session.execute(stmt_dish)
        menu = result_dish.scalars().first()
        stmt_submenu = select(Submenu).where(
            Submenu.menu_id == target_menu_id,
            Submenu.id == target_submenu_id,
        )
        result_submenu = await self.session.execute(stmt_submenu)
        submenu = result_submenu.scalars().first()

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

        new_dish = Dish(**dish_data.model_dump(), submenu_id=target_submenu_id)
        self.session.add(new_dish)
        await self.session.commit()
        await self.session.refresh(new_dish)
        return new_dish

    async def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> Dish:
        dish = await self.search_dish(target_menu_id, target_submenu_id, target_dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        return dish

    async def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
        dish_data: DishBaseSchema,
    ) -> Submenu:
        dish = await self.search_dish(target_menu_id, target_submenu_id, target_dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        for field, value in dish_data.model_dump().items():
            setattr(dish, field, value)

        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ) -> JSONResponse:
        dish = await self.search_dish(target_menu_id, target_submenu_id, target_dish_id)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        await self.session.delete(dish)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Dish {dish.title} deleted successfully"},
        )

    async def search_dish(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        target_dish_id: uuid.UUID,
    ):
        stmt = (
            select(Dish)
            .join(Submenu, Dish.submenu)
            .where(
                Submenu.menu_id == target_menu_id,
                Dish.submenu_id == target_submenu_id,
                Dish.id == target_dish_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
