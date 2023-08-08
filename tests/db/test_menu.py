from tests.conftest import client

prefix = "/api/v1"
test_data: dict[str, str] = {}


def test_get_all_menus():
    url = f"{prefix}/menus/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Создаем меню
def test_create_menu():
    url = f"{prefix}/menus/"
    data = {
        "title": "Test Menu",
        "description": "This is a test menu",
    }
    response = client.post(url, json=data)
    assert response.status_code == 201

    test_data["target_menu_id"] = response.json().get("id")
    test_data["target_menu_title"] = response.json().get("title")
    test_data["target_menu_description"] = response.json().get("description")

    assert test_data["target_menu_id"] is not None
    assert test_data["target_menu_title"] == "Test Menu"
    assert test_data["target_menu_description"] == "This is a test menu"


def test_get_menu():
    target_menu_id = test_data.get("target_menu_id")
    url = f"{prefix}/menus/{target_menu_id}/"
    response = client.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == target_menu_id
    assert response_json["title"] == test_data.get("target_menu_title")
    assert response_json["description"] == test_data.get("target_menu_description")


def test_update_menu():
    target_menu_id = test_data.get("target_menu_id")
    url = f"{prefix}/menus/{target_menu_id}/"
    data = {
        "title": "Updated Test Menu",
        "description": "This is an updated test menu",
    }
    response = client.patch(url, json=data)
    assert response.status_code == 200

    assert test_data["target_menu_title"] != data["title"]
    assert test_data["target_menu_description"] != data["description"]

    test_data["target_menu_title"] = data["title"]
    test_data["target_menu_description"] = data["description"]

    assert test_data["target_menu_title"] == response.json().get("title")
    assert test_data["target_menu_description"] == response.json().get("description")


def test_delete_menu():
    target_menu_id = test_data.get("target_menu_id")
    url = f"{prefix}/menus/{target_menu_id}/"
    response = client.delete(url)
    assert response.status_code == 200


def test_view_menu():
    target_menu_id = test_data.get("target_menu_id")
    url = f"{prefix}/menus/{target_menu_id}/"
    response = client.get(url)

    assert response.status_code == 404

    response_json = response.json()
    assert response_json["detail"] == "menu not found"
