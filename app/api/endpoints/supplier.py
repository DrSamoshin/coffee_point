from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.supplier import SupplierCreate, SupplierOut, SupplierUpdate
from app.crud import supplier as crud_supplier
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/suppliers', tags=['suppliers'])

@router.get("/", response_model=list[SupplierOut])
async def get_suppliers(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_suppliers = crud_supplier.get_suppliers(db)
    return db_suppliers

@router.get("/{supplier_id}/", response_model=SupplierOut)
async def get_supplier(supplier_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supplier = crud_supplier.get_supplier(db, supplier_id)
    return db_supplier

@router.post("/", response_model=SupplierOut)
async def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supplier = crud_supplier.create_supplier(db, supplier)
    return db_supplier

@router.put("/{supplier_id}/", response_model=SupplierOut)
async def update_supplier(supplier_id: UUID, supplier_update: SupplierUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supplier = crud_supplier.update_supplier(db, supplier_id, supplier_update)
    return db_supplier
