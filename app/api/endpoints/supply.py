from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.supply import SupplyCreate, SupplyOut, SupplyUpdate
from app.crud import supply as crud_supply
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/supplies', tags=['supplies'])

@router.get("/", response_model=list[SupplyOut])
async def get_supplies(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supplies = crud_supply.get_supplies(db)
    return db_supplies

@router.get("/{supply_id}/", response_model=SupplyOut)
async def get_supply(supply_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supply = crud_supply.get_supply(db, supply_id)
    return db_supply

@router.post("/", response_model=SupplyOut)
async def create_supply(supply: SupplyCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supply = crud_supply.create_supply(db, supply)
    return db_supply

@router.put("/{supply_id}/", response_model=SupplyOut)
async def update_supply(supply_id: UUID, supply_update: SupplyUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supply = crud_supply.update_supply(db, supply_id, supply_update)
    return db_supply
