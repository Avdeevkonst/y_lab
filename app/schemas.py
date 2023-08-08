import uuid

from pydantic import BaseModel, ConfigDict


class MenuBaseSchema(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class CreateMenuSchema(MenuBaseSchema):
    pass


class MenuResponse(MenuBaseSchema):
    id: uuid.UUID


class GetAllMenu(MenuResponse):
    submenus_count: int | None
    dishes_count: int | None


class UpdateMenuSchema(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class SubmenuBaseSchema(MenuBaseSchema):
    pass


class CreateSubmenuSchema(CreateMenuSchema):
    pass


class SubmenuResponse(MenuResponse):
    id: uuid.UUID


class UpdateSubmenuSchema(UpdateMenuSchema):
    pass


class FilteredSubmenuResponse(SubmenuBaseSchema):
    id: uuid.UUID
    dishes_count: int | None


class DishBaseSchema(BaseModel):
    title: str
    description: str
    price: str

    model_config = ConfigDict(from_attributes=True)


class CreateDishSchema(DishBaseSchema):
    pass


class DishResponse(DishBaseSchema):
    id: uuid.UUID


class UpdateDishSchema(DishBaseSchema):
    pass
