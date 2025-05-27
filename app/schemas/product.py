from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal

from app.schemas.category import CategoryOut


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
    category: CategoryOut

    model_config = {"from_attributes": True}

class ProductOnlineShopOut(BaseModel):
    id: UUID
    name: str
    price: Decimal
    image_url: Optional[str]
    category: CategoryOut

    model_config = {"from_attributes": True}

