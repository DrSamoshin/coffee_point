from uuid import UUID
from pydantic import BaseModel

class ProductOrderBase(BaseModel):
    product_id: UUID
    order_id: UUID

class ProductOrderCreate(ProductOrderBase):
    pass

class ProductOrderUpdate(ProductOrderBase):
    pass

class ProductOrderOut(ProductOrderBase):
    id: UUID

    model_config = {"from_attributes": True}

