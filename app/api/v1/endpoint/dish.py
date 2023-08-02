from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import schemas
from app.db.database import get_db
from app.db.models import Dish

router = APIRouter()


# Get dishes
@router.get("/{target_menu_id}/submenus/{target_submenu_id}/dishes")
def get_dishes(db: Session = Depends(get_db)):
    dishes = db.query(Dish).group_by(Dish.id).all()
    dishes_response = []
    for dish in dishes:
        dishes_response.append(
            {
                "id": dish.id,
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }
        )
    return JSONResponse(content=jsonable_encoder(dishes_response))


# Get a single dish
@router.get(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    response_model=schemas.DishResponse,
)
def get_dish(target_dish_id: str, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == target_dish_id).first()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return dish


@router.post(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DishResponse,
)
def create_dish(
        target_submenu_id: str,
        dish: schemas.CreateDishSchema,
        db: Session = Depends(get_db),
):
    dish_add = Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=target_submenu_id,
    )
    # (title=dish.title, description=dish.description,
    #             price=dish.price, submenu_id=target_submenu_id)
    db.add(dish_add)
    # breakpoint()
    db.commit()
    db.refresh(dish_add)
    return dish_add
    # dish.submenu_id = uuid.UUID(target_submenu_id)
    # dec_price = dish.price.quantize(Decimal('.01'))
    # dish.price = dec_price
    # new_dish = Dish(title=title)
    # breakpoint()
    # db.add(create)


@router.patch(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    response_model=schemas.DishResponse,
)
def update_dish(
        target_dish_id: str, dish: schemas.UpdateDishSchema, db: Session = Depends(get_db)
):
    dish_query = db.query(Dish).filter(Dish.id == target_dish_id)
    updated_dish = dish_query.first()

    if not updated_dish:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"No submenu with this id: {target_dish_id} found",
        )
    dish_query.update(dish.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_dish


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def delete_dish(target_dish_id: str, db: Session = Depends(get_db)):
    dish_query = db.query(Dish).filter(Dish.id == target_dish_id)
    dish = dish_query.first()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No dish with this id: {target_dish_id} found",
        )
    dish_query.delete(synchronize_session=False)
    db.commit()
    return dish
