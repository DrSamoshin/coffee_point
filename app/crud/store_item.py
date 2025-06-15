import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import StoreItem
from app.db.session import db_safe
from app.schemas.store_item import StoreItemCreate, StoreItemUpdate

@db_safe
def get_store_item(db: Session, store_item_id: UUID):
    return db.query(StoreItem).filter(StoreItem.id == store_item_id).first()

@db_safe
def get_store_items(db: Session):
    return db.query(StoreItem).filter(StoreItem.active == True).all()

@db_safe
def get_deactivated_store_items(db: Session):
    return db.query(StoreItem).filter(StoreItem.active == False).all()

@db_safe
def create_store_item(db: Session, store_item: StoreItemCreate):
    db_store_item = StoreItem(item_id=store_item.item_id,
                              supply_id=store_item.supply_id,
                              amount=store_item.amount,
                              price_per_item=store_item.price_per_item)
    db.add(db_store_item)
    db.commit()
    db.refresh(db_store_item)
    return db_store_item

@db_safe
def update_store_item(db: Session, store_item_id: UUID, updates: StoreItemUpdate):
    try:
        db_store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_store_item, field, value)
        db.commit()
        db.refresh(db_store_item)
        return db_store_item
    except Exception as error:
        logging.warning(error)

@db_safe
def deactivate_store_item(db: Session, db_store_item: StoreItem):
    db_store_item.active = False
    db.commit()
    db.refresh(db_store_item)

@db_safe
def activate_store_item(db: Session, store_item_id: UUID):
    db_store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id, StoreItem.active == False).first()
    if db_store_item:
        db_store_item.active = True
        db.commit()
        db.refresh(db_store_item)
    return db_store_item