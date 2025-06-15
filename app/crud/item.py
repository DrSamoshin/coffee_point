import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Item
from app.db.session import db_safe
from app.schemas.item import ItemCreate, ItemUpdate

@db_safe
def get_item(db: Session, item_id: UUID):
    logging.info(f"call method get_item")
    return db.query(Item).filter(Item.id == item_id).first()

@db_safe
def get_items(db: Session):
    logging.info(f"call method get_items")
    return db.query(Item).filter(Item.active == True).all()

@db_safe
def create_item(db: Session, item: ItemCreate):
    logging.info(f"call method create_item")
    db_item = Item(name=item.name,
                   measurement=item.measurement)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@db_safe
def update_item(db: Session, item_id: UUID, updates: ItemUpdate):
    logging.info(f"call method update_item")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as error:
        logging.warning(error)

