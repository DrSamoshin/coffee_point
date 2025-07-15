import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Item
from app.db.db_sessions import db_safe
from app.schemas.item import ItemCreate, ItemUpdate


@db_safe
def get_item(db: Session, item_id: UUID):
    logging.info("call method get_item")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"item: {db_item}")
        return db_item


@db_safe
def get_items(db: Session):
    logging.info("call method get_items")
    try:
        db_items = db.query(Item).filter(Item.active is True).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"items: {len(db_items)}")
        return db_items


@db_safe
def create_item(db: Session, item: ItemCreate):
    logging.info("call method create_item")
    try:
        db_item = db.query(Item).filter(Item.name == item.name).first()
        if not db_item:
            db_item = Item(name=item.name.strip(), measurement=item.measurement)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
        elif not db_item.active:
            db_item.active = True
            db.commit()
            db.refresh(db_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"item is created: {db_item}")
        return db_item


@db_safe
def update_item(db: Session, item_id: UUID, updates: ItemUpdate):
    logging.info("call method update_item")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"item is updated: {db_item}")
        return db_item


@db_safe
def delete_item(db: Session, item_id: UUID):
    logging.info("call method delete_item")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        db_item.active = False
        db.commit()
        db.refresh(db_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"item is deleted: {db_item}")
        return db_item
