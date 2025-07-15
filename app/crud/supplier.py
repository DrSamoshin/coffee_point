import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Supplier
from app.db.db_sessions import db_safe
from app.schemas.supplier import SupplierCreate, SupplierUpdate


@db_safe
def get_supplier(db: Session, supplier_id: UUID):
    logging.info("call method get_supplier")
    try:
        db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_supplier: {db_supplier}")
        return db_supplier


@db_safe
def get_suppliers(db: Session):
    logging.info("call method get_suppliers")
    try:
        db_suppliers = (
            db.query(Supplier)
            .filter(Supplier.deactivated == False)
            .order_by(Supplier.name)
            .all()
        )
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_suppliers: {len(db_suppliers)}")
        return db_suppliers


@db_safe
def get_deactivated_suppliers(db: Session):
    logging.info("call method get_deactivated_suppliers")
    try:
        db_suppliers = (
            db.query(Supplier)
            .filter(Supplier.deactivated == True)
            .order_by(Supplier.name)
            .all()
        )
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_suppliers: {len(db_suppliers)}")
        return db_suppliers


@db_safe
def create_supplier(db: Session, supplier: SupplierCreate):
    logging.info("call method create_supplier")
    try:
        db_supplier = db.query(Supplier).filter(Supplier.name == supplier.name).first()
        if not db_supplier:
            db_supplier = Supplier(name=supplier.name.strip())
            db.add(db_supplier)
            db.commit()
            db.refresh(db_supplier)
        elif db_supplier.deactivated:
            db_supplier.deactivated = False
            db.commit()
            db.refresh(db_supplier)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_supplier is created: {db_supplier}")
        return db_supplier


@db_safe
def update_supplier(db: Session, supplier_id: UUID, updates: SupplierUpdate):
    logging.info("call method update_supplier")
    try:
        db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_supplier, field, value)
        db.commit()
        db.refresh(db_supplier)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"db_supplier is updated: {db_supplier}")
        return db_supplier


@db_safe
def delete_supplier(db: Session, supplier_id: UUID):
    logging.info("call method delete_supplier")
    try:
        db_supplier = (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id, Supplier.deactivated == False)
            .first()
        )
        db_supplier.deactivated = True
        db.commit()
        db.refresh(db_supplier)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"supplier is deleted: {db_supplier}")
        return db_supplier


@db_safe
def activate_supplier(db: Session, supplier_id: UUID):
    logging.info("call method activate_supplier")
    try:
        db_supplier = (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id, Supplier.deactivated == True)
            .first()
        )
        db_supplier.deactivated = False
        db.commit()
        db.refresh(db_supplier)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"supplier is activated: {db_supplier}")
        return db_supplier
