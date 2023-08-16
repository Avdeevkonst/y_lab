import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.db.database import get_db
from app.db.models import Dish, Menu, Submenu
from app.schemas import (
    CreateSubmenuSchema,
    FilteredSubmenuResponse,
    SubmenuResponse,
    UpdateSubmenuSchema,
)


class SubMenuRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]):
        self.session: Session = session
        self.model = Submenu

    async def get_all(self, target_menu_id: uuid.UUID) -> list[SubmenuResponse]:
        stmt = select(Submenu).where(Submenu.menu_id == target_menu_id)
        result = await self.session.execute(stmt)
        submenus = result.scalars().fetchall()
        submenu_responses = []
        for submenu in submenus:
            dishes_query = select(func.count(Dish.id)).where(
                Submenu.menu_id == target_menu_id,
            )
            dishes_count = await self.session.execute(dishes_query)
            dishes_result = len(dishes_count.scalars().fetchall())
            submenu_response = SubmenuResponse(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=dishes_result,
            )
            submenu_responses.append(submenu_response)
        return submenu_responses

    async def create(
        self,
        target_menu_id: uuid.UUID,
        submenu_data: CreateSubmenuSchema,
    ) -> Submenu:
        stmt = select(Menu).where(Menu.id == target_menu_id)
        result = await self.session.execute(stmt)
        menu = result.scalars().first()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )
        new_submenu = Submenu(**submenu_data.model_dump(), menu_id=target_menu_id)
        self.session.add(new_submenu)
        await self.session.commit()
        await self.session.refresh(new_submenu)
        return new_submenu

    async def get(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
    ) -> FilteredSubmenuResponse:
        submenu = await self.search_submenu(target_menu_id, target_submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        dishes_query = select(func.count(Dish.id)).filter(
            Dish.submenu_id == target_submenu_id,
        )
        dishes_count = await self.session.execute(dishes_query)
        dishes_result = dishes_count.scalars().fetchall()
        return FilteredSubmenuResponse(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            menu_id=submenu.menu_id,
            dishes_count=dishes_result[0],
        )

    async def update(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
        submenu_data: UpdateSubmenuSchema,
    ) -> type[Submenu]:
        submenu = await self.search_submenu(target_menu_id, target_submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        submenu.title = submenu_data.title
        submenu.description = submenu_data.description
        await self.session.commit()
        await self.session.refresh(submenu)
        return submenu

    async def delete(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
    ) -> JSONResponse:
        submenu = await self.search_submenu(target_menu_id, target_submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        await self.session.delete(submenu)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Submenu {submenu.title} deleted successfully"},
        )

    async def search_submenu(
        self,
        target_menu_id: uuid.UUID,
        target_submenu_id: uuid.UUID,
    ):
        stmt = select(Submenu).where(
            Submenu.menu_id == target_menu_id,
            Submenu.id == target_submenu_id,
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
