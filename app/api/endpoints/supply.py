from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.supply import SupplyCreate, SupplyOut, SupplyUpdate
from app.crud import supply as crud_supply
from app.core.responses import response
from app.middleware.authentication import get_user_id_from_token

router = APIRouter(prefix='/supplies', tags=['supplies'])

@router.get("/", response_model=list[SupplyOut])
async def read_supplys(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_supply.get_supplys(db)

@router.get("/{supply_id}/", response_model=SupplyOut)
async def read_supply(supply_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supply = crud_supply.get_supply(db, supply_id)
    if not db_supply:
        return response("supply not found", 404)
    return db_supply

@router.post("/", response_model=SupplyOut)
async def create_supply(supply: SupplyCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supply = crud_supply.create_supply(db, supply)
    return db_supply

@router.put("/{supply_id}/", response_model=SupplyOut)
async def update_supply(supply_id: UUID, supply_update: SupplyUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_supply = crud_supply.get_supply(db, supply_id)
    if not db_supply:
        return response("supply not found", 404)
    db_supply = crud_supply.update_supply(db, db_supply, supply_update)
    return db_supply
