from httpx import AsyncClient

from app.schemas import MenuResponse

prefix = "/api/v1"
test_data: dict[str, str] = {}


async def test_get_all_menus(ac: AsyncClient):
    url = f"{prefix}/menus/"
    response = await ac.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_create_menu(ac: AsyncClient):
    url = f"{prefix}/menus/"
    data = {
        "title": "Test Menu",
        "description": "This is a test menu",
    }
    response = await ac.post(url, json=data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Menu"
    assert response.json()["description"] == "This is a test menu"


async def test_get_menu(ac: AsyncClient, default_menu: MenuResponse):
    url = f"{prefix}/menus/{default_menu.id}"
    response = await ac.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == default_menu.id
    assert response.json()["title"] == default_menu.title
    assert response.json()["description"] == default_menu.description


async def test_update_menu(ac: AsyncClient, default_menu: MenuResponse):
    url = f"{prefix}/menus/{default_menu.id}"
    data = {
        "title": "Updated Test Menu",
        "description": "This is an updated test menu",
    }
    response = await ac.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Menu"
    assert response.json()["description"] == "This is an updated test menu"


async def test_delete_menu(ac: AsyncClient, default_menu: MenuResponse):
    url = f"{prefix}/menus/{default_menu.id}"
    response_delete = await ac.delete(url)
    assert response_delete.status_code == 200
    response_get = await ac.get(url)
    assert response_get.status_code == 404
