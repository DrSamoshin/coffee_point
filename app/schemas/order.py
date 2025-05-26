
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

from app.core.consts import Type, PaymentMethod
from app.schemas.product import ProductOut


class OrderBase(BaseModel):
    price: Decimal
    date: datetime
    payment_method: PaymentMethod
    type: Type
    shift_id: UUID
    client_id: Optional[UUID] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: UUID
    active: bool

class OrderWithProductsOut(OrderOut):
    products: list[ProductOut]

    model_config = {"from_attributes": True}

