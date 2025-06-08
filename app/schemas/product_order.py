from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ProductOrderBase(BaseModel):
    product_id: UUID
    order_id: UUID
    count: int

class ProductOrderCreate(BaseModel):
    product_id: UUID
    count: int

class ProductOrderUpdate(BaseModel):
    product_id: UUID
    count: int
    product_order_id: Optional[UUID] = None

class ProductOrderOut(ProductOrderBase):
    id: UUID

    model_config = {"from_attributes": True}

