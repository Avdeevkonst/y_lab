import uuid
from app import schemas
from app.db.models import Dish, Submenu, Menu
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db.database import get_db

router = APIRouter()


# Get submenus
@router.get('/{target_menu_id}/submenus')
def get_submenus(db: Session = Depends(get_db)):
    submenus = db.query(Submenu).group_by(Submenu.id).all()
    submenu_response = []
    for submenu in submenus:
        dishes = db.query(Dish).filter(Dish.submenu_id == submenu.id).all()
        submenu_response.append({'id': submenu.id, 'title': submenu.title, 'description': submenu.description,
                                 'dishes_count': len(dishes)})
    return JSONResponse(content=jsonable_encoder(submenu_response))


# Get a single submenu
@router.get('/{target_menu_id}/submenus/{target_submenu_id}')
def get_submenu(target_submenu_id: str, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id).first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='submenu not found')
    dishes = db.query(Dish).filter(Dish.submenu_id == submenu.id).all()
    submenu_response = {'id': submenu.id, 'title': submenu.title, 'description': submenu.description,
                        'dishes_count': len(dishes)}
    return JSONResponse(content=jsonable_encoder(submenu_response))


@router.post('/{target_menu_id}/submenus', status_code=status.HTTP_201_CREATED, response_model=schemas.SubmenuResponse)
def create_submenu(target_menu_id: str, submenu: schemas.CreateSubmenuSchema, db: Session = Depends(get_db)):
    submenu.menu_id = uuid.UUID(target_menu_id)
    new_submenu = Submenu(**submenu.model_dump())
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.MenuResponse)
def update_submenu(target_submenu_id: str, submenu: schemas.UpdateMenuSchema, db: Session = Depends(get_db)):
    submenu_query = db.query(Submenu).filter(Submenu.id == target_submenu_id)
    updated_submenu = submenu_query.first()

    if not updated_submenu:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No submenu with this id: {target_submenu_id} found')
    submenu_query.update(submenu.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_submenu


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}', status_code=status.HTTP_200_OK)
def delete_submenu(target_submenu_id: str, db: Session = Depends(get_db)):
    submenu_query = db.query(Submenu).filter(Submenu.id == target_submenu_id)
    submenu = submenu_query.first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    db.delete(submenu)
    db.commit()
    return {"status": True,
            "message": "The submenu has been deleted"}
