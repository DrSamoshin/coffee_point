from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.crud import item as crud_item
from app.core.responses import response

router = APIRouter(prefix='/items', tags=['items'])

@router.get("/", response_model=list[ItemOut])
def read_items(db: Session = Depends(get_db)):
    return crud_item.get_items(db)

@router.get("/{item_id}", response_model=ItemOut)
def read_item(item_id: UUID, db: Session = Depends(get_db)):
    db_item = crud_item.get_item(db, item_id)
    if not db_item:
        return response("item not found", 404)
    return db_item

@router.post("/", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = crud_item.create_item(db, item)
    return db_item

@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: UUID, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud_item.get_item(db, item_id)
    if not db_item:
        return response("item not found", 404)
    db_item = crud_item.update_item(db, db_item, item_update)
    return db_item
