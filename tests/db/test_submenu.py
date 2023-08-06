from tests.conftest import client

prefix = "/api/v1"
test_data: dict[str, str] = {}


# Просматриваем список подменю
def test_get_all_submenus():
    target_menu_id = test_data.get("target_menu_id")
    url = f"{prefix}/menus/{target_menu_id}/submenus"
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Создаем подменю
def test_create_submenu():
    target_menu_id = test_data.get("target_menu_id")
    url = f"{prefix}/menus/{target_menu_id}/submenus"
    data = {
        "title": "Test Submenu",
        "description": "This is a test submenu",
    }
    response = client.post(url, json=data)

    assert response.status_code == 201

    test_data["target_submenu_id"] = response.json().get("id")
    test_data["target_submenu_title"] = response.json().get("title")
    test_data["target_submenu_description"] = response.json().get("description")

    assert test_data["target_submenu_id"] is not None
    assert test_data["target_submenu_title"] == "Test Submenu"
    assert test_data["target_submenu_description"] == "This is a test submenu"


# Просматриваем определенное подменю
def test_get_submenu():
    target_menu_id = test_data.get("target_menu_id")
    target_submenu_id = test_data.get("target_submenu_id")
    url = f"{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}"
    response = client.get(url)

    assert response.status_code == 200

    response_json = response.json()
    assert response_json["id"] == target_submenu_id
    assert response_json["title"] == test_data.get("target_submenu_title")
    assert response_json["description"] == test_data.get("target_submenu_description")


# Обновляем определенное подменю
def test_update_submenu():
    target_menu_id = test_data.get("target_menu_id")
    target_submenu_id = test_data.get("target_submenu_id")
    url = f"{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}"
    data = {
        "title": "Updated Submenu",
        "description": "This is an updated submenu",
    }
    response = client.patch(url, json=data)

    assert response.status_code == 200

    response_json = response.json()
    # Проверяем, что данные изменились
    assert response_json["title"] != test_data.get("target_submenu_title")
    assert response_json["description"] != test_data.get("target_submenu_description")

    # Сохраняем обновленные данные в словарь
    test_data["target_submenu_title"] = data["title"]
    test_data["target_submenu_description"] = data["description"]

    # Проверяем, что данные соответствуют обновленным данным
    assert test_data["target_submenu_title"] == response_json["title"]
    assert test_data["target_submenu_description"] == response_json["description"]


# Удаляем подменю
def test_delete_submenu():
    target_menu_id = test_data.get("target_menu_id")
    target_submenu_id = test_data.get("target_submenu_id")
    url = f"{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}"
    response = client.delete(url)

    assert response.status_code == 200


# Просматриваем определенное подменю
def test_get_once_submenu():
    target_menu_id = test_data.get("target_menu_id")
    target_submenu_id = test_data.get("target_submenu_id")
    url = f"{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}"
    response = client.get(url)

    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"
