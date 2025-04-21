from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    category_id: UUID
    price: Decimal

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: UUID

    model_config = {"from_attributes": True}

