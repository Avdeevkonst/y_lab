from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.services.data import DataService
from app.schemas import NestedDataMenu

router = APIRouter()


@router.get("/", response_model=NestedDataMenu)
async def get_all_data(
    data: Annotated[DataService, Depends()],
):
    return await data.get_all()
