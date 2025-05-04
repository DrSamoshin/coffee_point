from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.store_item import StoreItemCreate, StoreItemOut, StoreItemUpdate
from app.crud import store_item as crud_store_item
from app.core.responses import response
from app.middleware.authentication import get_user_id_from_token

router = APIRouter(prefix='/store_items', tags=['store_items'])

@router.get("/", response_model=list[StoreItemOut])
def read_store_items(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_store_item.get_store_items(db)

@router.get("/{store_item_id}", response_model=StoreItemOut)
def read_store_item(store_item_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.get_store_item(db, store_item_id)
    if not db_store_item:
        return response("store_item not found", 404)
    return db_store_item

@router.post("/", response_model=StoreItemOut)
def create_store_item(store_item: StoreItemCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.create_store_item(db, store_item)
    return db_store_item

@router.put("/{store_item_id}", response_model=StoreItemOut)
def update_store_item(store_item_id: UUID, store_item_update: StoreItemUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.get_store_item(db, store_item_id)
    if not db_store_item:
        return response("store_item not found", 404)
    db_store_item = crud_store_item.update_store_item(db, db_store_item, store_item_update)
    return db_store_item
