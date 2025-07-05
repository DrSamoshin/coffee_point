import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Client
from app.db.db_sessions import db_safe
from app.schemas.client import ClientCreate, ClientUpdate

@db_safe
def get_client(db: Session, client_id: UUID):
    logging.info(f"call method get_client")
    try:
        db_client = db.query(Client).filter(Client.id == client_id, Client.deactivated == False).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"client: {db_client}")
        return db_client

@db_safe
def get_clients(db: Session):
    logging.info(f"call method get_clients")
    try:
        db_clients = db.query(Client).filter(Client.deactivated == False).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"clients: {len(db_clients)}")
        return db_clients

@db_safe
def create_client(db: Session, client: ClientCreate):
    logging.info(f"call method create_client")
    try:
        db_client = Client(name=client.name)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"client is created: {db_client}")
        return db_client

@db_safe
def update_client(db: Session, client_id: UUID, updates: ClientUpdate):
    logging.info(f"call method update_client")
    try:
        db_client = db.query(Client).filter(Client.id == client_id, Client.deactivated == False).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_client, field, value)
        db.commit()
        db.refresh(db_client)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"client is updated: {db_client}")
        return db_client
