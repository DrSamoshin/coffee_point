from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.store_item import StoreItemCreate, StoreItemOut, StoreItemUpdate, CalculationStoreItemOut
from app.crud import store_item as crud_store_item
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/store-items', tags=['store_items'])

@router.get("/", response_model=list[StoreItemOut])
async def get_store_items(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_items = crud_store_item.get_store_items(db)
    return db_store_items

@router.get("/calculation/", response_model=list[CalculationStoreItemOut])
async def get_store_items_calculation(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_items = crud_store_item.get_store_items_calculation(db)
    return db_store_items

@router.get("/{store_item_id}/", response_model=StoreItemOut)
async def get_store_item(store_item_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.get_store_item(db, store_item_id)
    return db_store_item

@router.post("/add/", response_model=StoreItemOut)
async def add_store_item(store_item: StoreItemCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.add_store_item(db, store_item)
    return db_store_item

@router.post("/remove/", response_model=StoreItemOut)
async def remove_store_item(store_item: StoreItemCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.remove_store_item(db, store_item)
    return db_store_item

@router.put("/{store_item_id}/", response_model=StoreItemOut)
async def update_store_item(store_item_id: UUID, store_item_update: StoreItemUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_store_item = crud_store_item.update_store_item(db, store_item_id, store_item_update)
    return db_store_item
