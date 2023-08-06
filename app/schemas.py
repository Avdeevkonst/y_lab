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


class UpdateMenuSchema(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class FilteredMenuResponse(MenuBaseSchema):
    id: uuid.UUID


class SubmenuBaseSchema(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class CreateSubmenuSchema(SubmenuBaseSchema):
    pass


class SubmenuResponse(SubmenuBaseSchema):
    id: uuid.UUID


class UpdateSubmenuSchema(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class FilteredSubmenuResponse(SubmenuBaseSchema):
    id: uuid.UUID


class DishBaseSchema(BaseModel):
    title: str
    description: str
    price: str
    submenu_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateDishSchema(DishBaseSchema):
    pass


class DishResponse(DishBaseSchema):
    id: uuid.UUID


class UpdateDishSchema(DishBaseSchema):
    pass
