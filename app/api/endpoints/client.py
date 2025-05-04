from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.crud import client as crud_client
from app.core.responses import response
from app.middleware.authentication import get_user_id_from_token

router = APIRouter(prefix='/clients', tags=['clients'])

@router.get("/", response_model=list[ClientOut])
def read_clients(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_client.get_clients(db)

@router.get("/{client_id}", response_model=ClientOut)
def read_client(client_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        return response("client not found", 404)
    return db_client

@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.create_client(db, client)
    return db_client

@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: UUID, client_update: ClientUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        return response("client not found", 404)
    db_client = crud_client.update_client(db, db_client, client_update)
    return db_client
