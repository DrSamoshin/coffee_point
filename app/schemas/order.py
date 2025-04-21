from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"

class Type(str, Enum):
    dine_in = "dine_in"
    delivery = "delivery"
    takeout = "takeout"

class OrderBase(BaseModel):
    price: Decimal
    date: datetime
    payment_method: PaymentMethod
    kind: Type
    shift_id: UUID
    client_id: Optional[UUID] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}

