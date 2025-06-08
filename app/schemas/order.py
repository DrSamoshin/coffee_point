
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

from app.core.consts import OrderType, OrderPaymentMethod, OrderStatus
from app.schemas.product import ProductOrderOut
from app.schemas.product_order import ProductOrderCreate, ProductOrderUpdate


class OrderBase(BaseModel):
    price: Decimal
    date: datetime
    payment_method: OrderPaymentMethod
    type: OrderType
    status: OrderStatus
    shift_id: UUID
    client_id: Optional[UUID] = None

class OrderCreate(OrderBase):
    products: list[ProductOrderCreate]

class OrderUpdate(BaseModel):
    price: Optional[Decimal] = None
    date: Optional[datetime] = None
    payment_method: Optional[OrderPaymentMethod] = None
    type: Optional[OrderType] = None
    client_id: Optional[UUID] = None
    products: Optional[list[ProductOrderUpdate]] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderOut(OrderBase):
    id: UUID
    active: bool

class ShiftOrderOut(BaseModel):
    id: UUID
    active: bool
    price: Decimal
    date: datetime
    payment_method: OrderPaymentMethod
    type: OrderType
    status: OrderStatus
    client_id: Optional[UUID] = None
    products: list[ProductOrderOut]

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        },
        from_attributes=True
    )
