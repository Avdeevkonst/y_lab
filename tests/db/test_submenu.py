from tests.conftest import client
from tests.db.test_menu import prefix
from tests.schemas import Menu as MenuResponse
from tests.schemas import Submenu as SubmenuResponse

test_data: dict[str, str] = {}


def test_create_menu():
    url = f"{prefix}/menus/"
    data = {
        "title": "Test Menu",
        "description": "This is a test menu",
    }
    response = client.post(url, json=data)

    assert response.status_code == 201

    MenuResponse.id = response.json().get("id")


# Просматриваем список подменю
def test_get_all_submenus():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Создаем подменю
def test_create_submenu():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus"
    data = {
        "title": "Test Submenu",
        "description": "This is a test submenu",
    }
    response = client.post(url, json=data)
    SubmenuResponse.id = response.json().get("id")
    SubmenuResponse.title = response.json().get("title")
    SubmenuResponse.description = response.json().get("description")
    assert response.status_code == 201


# Просматриваем определенное подменю
def test_get_submenu():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}"
    response = client.get(url)

    assert response.status_code == 200

    response_json = response.json()
    assert response_json["id"] == SubmenuResponse.id
    assert response_json["title"] == SubmenuResponse.title
    assert response_json["description"] == SubmenuResponse.description


# Обновляем определенное подменю
def test_update_submenu():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}"
    data = {
        "title": "Updated Submenu",
        "description": "This is an updated submenu",
    }
    response = client.patch(url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Submenu"
    assert response.json()["description"] == "This is an updated submenu"


# Удаляем подменю
def test_delete_submenu():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}"
    response = client.delete(url)
    assert response.status_code == 200
