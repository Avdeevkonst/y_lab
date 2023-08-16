import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.db.database import Base, engine
from app.main import app
from app.schemas import DishResponse, MenuResponse, SubmenuResponse


@pytest.fixture(autouse=True)
async def _prepare_database() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def ac():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac


@pytest.fixture()
async def default_menu(ac: AsyncClient) -> MenuResponse:
    return MenuResponse.model_validate(
        (
            await ac.post(
                "/api/v1/menus/",
                json={
                    "title": "summer menu",
                    "description": "menu",
                },
            )
        ).json(),
    )


@pytest.fixture()
async def default_submenu(
    ac: AsyncClient,
    default_menu: MenuResponse,
) -> SubmenuResponse:
    return SubmenuResponse.model_validate(
        (
            await ac.post(
                f"/api/v1/menus/{default_menu.id}/submenus/",
                json={
                    "title": "georgian dishes",
                    "description": "georgian dishes",
                },
            )
        ).json(),
    )


@pytest.fixture()
async def default_dish(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
) -> DishResponse:
    return DishResponse.model_validate(
        (
            await ac.post(
                f"/api/v1/menus/{default_menu.id}/submenus/{default_submenu.id}/dishes/",
                json={
                    "title": "kharcho",
                    "description": "hearty soup",
                    "price": "100.25",
                },
            )
        ).json(),
    )
