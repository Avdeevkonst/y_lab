from tests.conftest import *


def test_get_all_menus():
    res = client.get("/api/v1/menus/")
    assert res.status_code == 200
    assert res.json() == []


def test_create_menu():
    global menu_id
    res = client.post("/api/v1/menus/", json={"title": "My menu 1", "description": "My menu description 1"})
    assert res.status_code == 201
    menu_id = res.json()["id"]
    res = client.get("/api/v1/menus")
    assert len(res.json()) == 1


def test_update_menu():
    global menu_id
    res = client.patch(f"/api/v1/menus/{menu_id}", json={"title": "My menu 2", "description": "My menu description 2"})
    assert res.status_code == 200
    res = client.get(f"/api/v1/menus/{menu_id}")
    assert res.json()["title"] == "My menu 2"
    assert res.json()["description"] == "My menu description 2"


def test_get_all_submenus():
    global menu_id
    res = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert res.status_code == 200
    assert res.json() == []


def test_create_submenu():
    global menu_id
    global submenu_id
    res = client.post(f"/api/v1/menus/{menu_id}/submenus/",
                      json={"title": "My submenu 1", "description": "My submenu description 1"})
    assert res.status_code == 201
    submenu_id = res.json()["id"]
    res = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert len(res.json()) == 1


def test_update_submenu():
    global menu_id
    global submenu_id
    res = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/",
                       json={"title": "My submenu 2", "description": "My submenu description 2"})
    assert res.status_code == 200
    res = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
    assert res.json()["title"] == "My submenu 2"
    assert res.json()["description"] == "My submenu description 2"


def test_get_all_dishes():
    global menu_id
    global submenu_id
    res = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert res.status_code == 200
    assert res.json() == []


def test_create_dish():
    global menu_id
    global submenu_id
    global dish_id
    res = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/",
                      json={"title": "My dish 1", "description": "My dish description 1", "price": "12.50"})
    assert res.status_code == 201
    dish_id = res.json()["id"]
    res = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert len(res.json()) == 1


def test_update_dish():
    global menu_id
    global submenu_id
    global dish_id
    res = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/",
                       json={"title": "My updated dish 1", "description": "My updated dish description 1",
                             "price": "14.50"})
    assert res.status_code == 200
    res = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/")
    assert res.json()["title"] == "My updated dish 1"
    assert res.json()["description"] == "My updated dish description 1"
    assert res.json()["price"] == "14.50"


def test_delete_dish():
    global menu_id
    global submenu_id
    global dish_id
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/")
    assert response.status_code == 200
    res = client.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert res.json() == []


def test_delete_submenu():
    global menu_id
    global submenu_id
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
    assert response.status_code == 200
    res = client.get("/api/v1/menus/{menu_id}/submenus/")
    assert res.json() == []


def test_delete_menu():
    global menu_id
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    res = client.get("/api/v1/menus/")
    assert res.json() == []
