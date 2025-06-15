from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.crud import item as crud_item
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/items', tags=['items'])

@router.get("/", response_model=list[ItemOut])
async def get_items(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_items = crud_item.get_items(db)
    return db_items

@router.get("/{item_id}/", response_model=ItemOut)
async def get_item(item_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_item = crud_item.get_item(db, item_id)
    return db_item

@router.post("/", response_model=ItemOut)
async def create_item(item: ItemCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_item = crud_item.create_item(db, item)
    return db_item

@router.put("/{item_id}/", response_model=ItemOut)
async def update_item(item_id: UUID, item_update: ItemUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_item = crud_item.update_item(db, item_id, item_update)
    return db_item
