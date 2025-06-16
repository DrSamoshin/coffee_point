import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import StoreItem
from app.db.session import db_safe
from app.schemas.store_item import StoreItemCreate, StoreItemUpdate

@db_safe
def get_store_item(db: Session, store_item_id: UUID):
    logging.info(f"call method get_store_item")
    try:
        store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item: {store_item}")
        return store_item

@db_safe
def get_store_items(db: Session):
    logging.info(f"call method get_store_items")
    try:
        store_items = db.query(StoreItem).filter(StoreItem.active == True).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_items: {len(store_items)}")
        return store_items

@db_safe
def create_store_item(db: Session, store_item: StoreItemCreate):
    logging.info(f"call method create_store_item")
    try:
        db_store_item = StoreItem(item_id=store_item.item_id,
                                  supply_id=store_item.supply_id,
                                  amount=store_item.amount,
                                  price_per_item=store_item.price_per_item)
        db.add(db_store_item)
        db.commit()
        db.refresh(db_store_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item is created: {db_store_item}")
        return db_store_item

@db_safe
def update_store_item(db: Session, store_item_id: UUID, updates: StoreItemUpdate):
    logging.info(f"call method update_store_item")
    try:
        db_store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_store_item, field, value)
        db.commit()
        db.refresh(db_store_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item is updated: {db_store_item}")
        return db_store_item
