import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Supply
from app.db.session import db_safe
from app.schemas.supply import SupplyCreate, SupplyUpdate

@db_safe
def get_supply(db: Session, supply_id: UUID):
    return db.query(Supply).filter(Supply.id == supply_id).first()

@db_safe
def get_supplies(db: Session):
    return db.query(Supply).filter(Supply.active == True).all()

@db_safe
def get_deactivated_supplys(db: Session):
    return db.query(Supply).filter(Supply.active == False).all()

@db_safe
def create_supply(db: Session, supply: SupplyCreate):
    db_supply = Supply(date=supply.date,
                       supplier_id=supply.supplier_id)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply

@db_safe
def update_supply(db: Session, supply_id: UUID, updates: SupplyUpdate):
    try:
        db_supply = db.query(Supply).filter(Supply.id == supply_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_supply, field, value)
        db.commit()
        db.refresh(db_supply)
        return db_supply
    except Exception as error:
        logging.warning(error)

@db_safe
def deactivate_supply(db: Session, db_supply: Supply):
    db_supply.active = False
    db.commit()
    db.refresh(db_supply)

@db_safe
def activate_supply(db: Session, supply_id: UUID):
    db_supply = db.query(Supply).filter(Supply.id == supply_id, Supply.active == False).first()
    if db_supply:
        db_supply.active = True
        db.commit()
        db.refresh(db_supply)
    return db_supply
