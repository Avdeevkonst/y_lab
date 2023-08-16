from httpx import AsyncClient

from app.schemas import DishResponse, MenuResponse, SubmenuResponse


async def test_get_all_data(
    ac: AsyncClient,
    default_menu: MenuResponse,
    default_submenu: SubmenuResponse,
    default_dish: DishResponse,
):
    url = "/api/v1/get-linked-list/"
    response = await ac.get(url)
    assert response.status_code == 200
