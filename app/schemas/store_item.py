from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal


class StoreItemBase(BaseModel):
    item_id: UUID
    supply_id: UUID
    amount: Decimal
    price_per_item: Decimal

class StoreItemCreate(StoreItemBase):
    pass

class StoreItemUpdate(StoreItemBase):
    pass

class StoreItemOut(StoreItemBase):
    id: UUID

    model_config = {"from_attributes": True}

