from tests.conftest import client
from tests.db.test_menu import prefix
from tests.schemas import Dish as DishResponse
from tests.schemas import Menu as MenuResponse
from tests.schemas import Submenu as SubmenuResponse


def test_create_menu():
    url = f"{prefix}/menus/"
    data = {
        "title": "Test Menu",
        "description": "This is a test menu",
    }
    response = client.post(url, json=data)

    assert response.status_code == 201

    MenuResponse.id = response.json().get("id")


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


def test_get_dishes():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}/dishes"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


def test_create_dish():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}/dishes"
    data = {
        "title": "Test Dish",
        "description": "This is a test dish",
        "price": "10.99",
    }
    response = client.post(url, json=data)
    DishResponse.id = response.json().get("id")
    DishResponse.title = response.json().get("title")
    DishResponse.description = response.json().get("description")
    DishResponse.price = response.json().get("price")
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["title"]
    assert response.json()["description"]
    assert response.json()["price"]


def test_update_dish():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}/dishes/{DishResponse.id}"
    data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
    }
    response = client.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "My updated dish 1"
    assert response.json()["description"] == "My updated dish description 1"
    assert response.json()["price"] == "14.50"


def test_delete_dish():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}/dishes/{DishResponse.id}"
    response = client.delete(url)
    assert response.status_code == 200


def test_delete_submenu():
    url = f"{prefix}/menus/{MenuResponse.id}/submenus/{SubmenuResponse.id}"
    response = client.delete(url)

    assert response.status_code == 200


def test_delete_menu():
    url = f"{prefix}/menus/{MenuResponse.id}/"
    response = client.delete(url)
    assert response.status_code == 200
