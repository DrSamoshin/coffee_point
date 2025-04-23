from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Item
from app.schemas.item import ItemCreate, ItemUpdate

def get_item(db: Session, item_id: UUID):
    return db.query(Item).filter(Item.id == item_id).first()

def get_item_by_name(db: Session, item_name: UUID):
    return db.query(Item).filter(Item.name == item_name).first()

def get_items(db: Session):
    return db.query(Item).filter(Item.active == True).all()

def get_deactivated_items(db: Session):
    return db.query(Item).filter(Item.active == False).all()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name,
                   measurement=item.measurement)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Item, updates: ItemUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def deactivate_item(db: Session, db_item: Item):
    db_item.active = False
    db.commit()
    db.refresh(db_item)

def activate_item(db: Session, item_id: UUID):
    db_item = db.query(Item).filter(Item.id == item_id, Item.active == False).first()
    if db_item:
        db_item.active = True
        db.commit()
        db.refresh(db_item)
    return db_item
