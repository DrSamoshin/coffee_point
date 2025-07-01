
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, Union
from decimal import Decimal

from app.core.consts import OrderType, OrderPaymentMethod, OrderStatus
from app.schemas.product import ProductOrderOut
from app.schemas.product_order import ProductOrderCreate, ProductOrderUpdate


class OrderBase(BaseModel):
    price: Decimal
    discount:Decimal
    payment_method: OrderPaymentMethod
    type: OrderType
    status: OrderStatus
    client_id: Optional[UUID] = None

class OrderCreate(OrderBase):
    debit: bool
    products: list[ProductOrderCreate]

class OrderUpdate(BaseModel):
    price: Decimal
    discount: Decimal
    payment_method: OrderPaymentMethod
    type: OrderType
    client_id: Optional[UUID] = None
    products: list[ProductOrderUpdate]

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderOut(OrderBase):
    id: UUID
    debit: bool
    date: datetime
    order_number: int

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        },
        from_attributes=True
    )

class ShiftOrderOut(BaseModel):
    id: UUID
    debit: bool
    price: Decimal
    discount: Decimal
    date: datetime
    payment_method: OrderPaymentMethod
    type: OrderType
    status: OrderStatus
    client_id: Optional[UUID] = None
    order_number: int
    products: list[ProductOrderOut]

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        },
        from_attributes=True
    )
