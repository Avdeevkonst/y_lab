from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.services.data import DataService

router = APIRouter()


@router.get(
    "/",
)
async def get_all_data(
    data: Annotated[DataService, Depends()],
):
    return await data.get_all()
