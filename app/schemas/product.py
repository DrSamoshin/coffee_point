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
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    price: Optional[Decimal] = None
    online_shop: Optional[bool] = None
    image_url: Optional[str] = None


class ProductFullInfoOut(ProductBase):
    id: UUID
    active: bool
    category: CategoryOut

    model_config = {"from_attributes": True}

class ProductOut(BaseModel):
    id: UUID
    name: str
    price: Decimal
    online_shop: bool
    category: CategoryOut
    image_url: Optional[str] = None

    model_config = {"from_attributes": True}

class ProductOrderOut(BaseModel):
    id: UUID
    name: str
    price: Decimal
    product_order_id: UUID
    count: int

    model_config = {"from_attributes": True}

