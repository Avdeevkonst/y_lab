from httpx import AsyncClient

from app.schemas import DishResponse, MenuResponse, SubmenuResponse
from tests.db.test_menu import prefix


async def test_get_dishes(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}/dishes/"
    response = await ac.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_create_dish(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}/dishes/"
    data = {
        "title": "Test Dish",
        "description": "This is a test dish",
        "price": "10.99",
    }
    response = await ac.post(url, json=data)
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["title"] == "Test Dish"
    assert response.json()["description"] == "This is a test dish"
    assert response.json()["price"] == "10.99"


async def test_update_dish(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
    default_dish: DishResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}/dishes/{default_dish.id}"
    data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
    }
    response = await ac.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "My updated dish 1"
    assert response.json()["description"] == "My updated dish description 1"
    assert response.json()["price"] == "14.50"


async def test_delete_dish(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
    default_dish: DishResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}/dishes/{default_dish.id}"
    response = await ac.delete(url)
    assert response.status_code == 200
