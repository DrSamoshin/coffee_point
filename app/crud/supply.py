import logging
from uuid import UUID
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models import Supply
from app.db.session import db_safe
from app.schemas.supply import SupplyCreate, SupplyUpdate

@db_safe
def get_supply(db: Session, supply_id: UUID):
    logging.info(f"call method get_supply")
    try:
        db_supply = db.query(Supply).filter(Supply.id == supply_id).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_supply: {db_supply}")
        return db_supply

@db_safe
def get_supplies(db: Session):
    logging.info(f"call method get_supplies")
    try:
        db_supplies = db.query(Supply).filter(Supply.active == True).order_by(desc(Supply.date)).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_supplies: {len(db_supplies)}")
        return db_supplies

@db_safe
def create_supply(db: Session, supply: SupplyCreate):
    logging.info(f"call method create_supply")
    try:
        db_supply = Supply(date=supply.date,
                           supplier_id=supply.supplier_id)
        db.add(db_supply)
        db.commit()
        db.refresh(db_supply)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"supply is created: {db_supply}")
        return db_supply

@db_safe
def update_supply(db: Session, supply_id: UUID, updates: SupplyUpdate):
    logging.info(f"call method update_supply")
    try:
        db_supply = db.query(Supply).filter(Supply.id == supply_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_supply, field, value)
        db.commit()
        db.refresh(db_supply)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"supply is updated: {db_supply}")
        return db_supply
