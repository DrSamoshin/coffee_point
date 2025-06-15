from pydantic import BaseModel
from uuid import UUID

class ClientBase(BaseModel):
    name: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: UUID
    deactivated: bool

    model_config = {"from_attributes": True}