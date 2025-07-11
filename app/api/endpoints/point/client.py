from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.db_sessions import get_point_db
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.crud import client as crud_client
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/clients', tags=['clients'])

@router.get("/", response_model=list[ClientOut])
async def get_clients(db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.get_clients(db)
    return db_client

@router.get("/{client_id}/", response_model=ClientOut)
async def get_client(client_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.get_client(db, client_id)
    return db_client

@router.post("/", response_model=ClientOut)
async def create_client(client: ClientCreate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.create_client(db, client)
    return db_client

@router.put("/{client_id}/", response_model=ClientOut)
async def update_client(client_id: UUID, client_update: ClientUpdate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.update_client(db, client_id, client_update)
    return db_client
