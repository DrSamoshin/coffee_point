from uuid import UUID
from pydantic import BaseModel
from app.core.consts import ItemMeasurements


class ItemBase(BaseModel):
    name: str
    measurement: ItemMeasurements


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemOut(ItemBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}
