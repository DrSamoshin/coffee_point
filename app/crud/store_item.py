from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import StoreItem
from app.schemas.store_item import StoreItemCreate, StoreItemUpdate

def get_store_item(db: Session, store_item_id: UUID):
    return db.query(StoreItem).filter(StoreItem.id == store_item_id).first()

def get_store_items(db: Session):
    return db.query(StoreItem).filter(StoreItem.active == True).all()

def get_deactivated_store_items(db: Session):
    return db.query(StoreItem).filter(StoreItem.active == False).all()

def create_store_item(db: Session, store_item: StoreItemCreate):
    db_store_item = StoreItem(item_id=store_item.item_id,
                              supply_id=store_item.supply_id,
                              amount=store_item.amount,
                              price_per_item=store_item.price_per_item)
    db.add(db_store_item)
    db.commit()
    db.refresh(db_store_item)
    return db_store_item

def update_store_item(db: Session, db_store_item: StoreItem, updates: StoreItemUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_store_item, field, value)
    db.commit()
    db.refresh(db_store_item)
    return db_store_item

def deactivate_store_item(db: Session, db_store_item: StoreItem):
    db_store_item.active = False
    db.commit()
    db.refresh(db_store_item)

def activate_store_item(db: Session, store_item_id: UUID):
    db_store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id, StoreItem.active == False).first()
    if db_store_item:
        db_store_item.active = True
        db.commit()
        db.refresh(db_store_item)
    return db_store_item