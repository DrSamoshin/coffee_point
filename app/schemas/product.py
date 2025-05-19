from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    category_id: UUID
    price: Decimal
    online_shop: bool
    image_url: Optional[str]

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}

