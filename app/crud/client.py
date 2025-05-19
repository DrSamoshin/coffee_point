from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Client
from app.db.session import db_safe
from app.schemas.client import ClientCreate, ClientUpdate

@db_safe
def get_client(db: Session, client_id: UUID):
    return db.query(Client).filter(Client.id == client_id, Client.active == True).first()

@db_safe
def get_clients(db: Session):
    return db.query(Client).filter(Client.active == True).all()

@db_safe
def create_client(db: Session, client: ClientCreate):
    db_client = Client(name=client.name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@db_safe
def update_client(db: Session, db_client: Client, updates: ClientUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_client, field, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@db_safe
def delete_client(db: Session, db_client: Client):
    db.delete(db_client)
    db.commit()

@db_safe
def deactivate_client(db: Session, db_client: Client):
    db_client.active = False
    db.commit()
    db.refresh(db_client)

@db_safe
def activate_client(db: Session, client_id: UUID):
    db_client = db.query(Client).filter(Client.id == client_id, Client.active == False).first()
    if db_client:
        db_client.active = True
        db.commit()
        db.refresh(db_client)
    return db_client
