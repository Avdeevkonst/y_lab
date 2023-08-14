from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.database import get_db
from app.db.models import Menu, Submenu


class DataRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]):
        self.session: Session = session

    async def get_all(self):
        result = await self.session.execute(
            select(Menu).options(
                selectinload(Menu.submenu).selectinload(Submenu.dishes),
            ),
        )
        menus = result.scalars().all()
        return [
            {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "submenus": [
                    {
                        "id": submenu.id,
                        "title": submenu.title,
                        "description": submenu.description,
                        "dishes": [
                            {
                                "id": dish.id,
                                "title": dish.title,
                                "description": dish.description,
                                "price": dish.price,
                            }
                            for dish in submenu.dishes
                        ],
                    }
                    for submenu in menu.submenu
                ],
            }
            for menu in menus
        ]
