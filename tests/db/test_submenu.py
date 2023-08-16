from httpx import AsyncClient

from app.schemas import MenuResponse, SubmenuResponse
from tests.db.test_menu import prefix


async def test_get_all_submenus(ac: AsyncClient, default_menu: MenuResponse):
    url = f"{prefix}/menus/{default_menu.id}/submenus/"
    response = await ac.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_create_submenu(ac: AsyncClient, default_menu: MenuResponse):
    url = f"{prefix}/menus/{default_menu.id}/submenus/"
    data = {
        "title": "Test Submenu",
        "description": "This is a test submenu",
    }
    response = await ac.post(url, json=data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Submenu"
    assert response.json()["description"] == "This is a test submenu"


async def test_get_submenu(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}"
    response = await ac.get(url)

    assert response.status_code == 200
    assert response.json()["title"] == default_submenu.title
    assert response.json()["description"] == default_submenu.description


async def test_update_submenu(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}"
    data = {
        "title": "Updated Submenu",
        "description": "This is an updated submenu",
    }
    response = await ac.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Submenu"
    assert response.json()["description"] == "This is an updated submenu"


async def test_delete_submenu(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
):
    url = f"{prefix}/menus/{default_menu.id}/submenus/{default_submenu.id}"
    response_delete = await ac.delete(url)
    assert response_delete.status_code == 200
    response_get = await ac.get(url)
    assert response_get.status_code == 404
