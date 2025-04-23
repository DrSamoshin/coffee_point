from uuid import UUID
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    measurement: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}

