from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class SupplyBase(BaseModel):
    date: datetime
    supplier_id: Optional[UUID] = None


class SupplyCreate(SupplyBase):
    pass


class SupplyUpdate(SupplyBase):
    pass


class SupplyOut(SupplyBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}
