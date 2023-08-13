import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import func
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
        submenus = (
            await self.session.query(Submenu).filter(Submenu.menu_id == target_menu_id).all()
        )
        submenu_responses = []

        for submenu in submenus:
            dishes_count = (
                await self.session.query(func.count(Dish.id))
                .filter(Dish.submenu_id == submenu.id)
                .scalar()
            )

            submenu_response = SubmenuResponse(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=dishes_count,
            )

            submenu_responses.append(submenu_response)

        return submenu_responses

    async def create(
            self,
            target_menu_id: uuid.UUID,
            submenu_data: CreateSubmenuSchema,
    ) -> Submenu:
        menu = await self.session.query(Menu).filter(Menu.id == target_menu_id).first()

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
        submenu = (
            await self.session.query(Submenu)
            .filter(Submenu.id == target_submenu_id, Submenu.menu_id == target_menu_id)
            .first()
        )
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        dishes_count = (
            await self.session.query(func.count(Dish.id))
            .filter(Dish.submenu_id == target_submenu_id)
            .scalar()
        )

        return FilteredSubmenuResponse(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            menu_id=submenu.menu_id,
            dishes_count=dishes_count,
        )

    async def update(
            self,
            target_menu_id: uuid.UUID,
            target_submenu_id: uuid.UUID,
            submenu_data: UpdateSubmenuSchema,
    ) -> type[Submenu]:
        submenu = (
            await self.session.query(Submenu)
            .filter(Submenu.id == target_submenu_id, Submenu.menu_id == target_menu_id)
            .first()
        )
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
        submenu = (
            await self.session.query(Submenu)
            .filter(Submenu.id == target_submenu_id, Submenu.menu_id == target_menu_id)
            .first()
        )

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
