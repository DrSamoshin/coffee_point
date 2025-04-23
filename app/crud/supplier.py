from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

def get_supplier(db: Session, supplier_id: UUID):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_suppliers(db: Session):
    return db.query(Supplier).filter(Supplier.active == True).all()

def get_deactivated_suppliers(db: Session):
    return db.query(Supplier).filter(Supplier.active == False).all()

def create_supplier(db: Session, supplier: SupplierCreate):
    db_supplier = Supplier(name=supplier.name)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(db: Session, db_supplier: Supplier, updates: SupplierUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_supplier, field, value)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def deactivate_supplier(db: Session, db_supplier: Supplier):
    db_supplier.active = False
    db.commit()
    db.refresh(db_supplier)

def activate_supplier(db: Session, supplier_id: UUID):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.active == False).first()
    if db_supplier:
        db_supplier.active = True
        db.commit()
        db.refresh(db_supplier)
    return db_supplier
