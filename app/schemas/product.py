from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from app.core.consts import OrderType, OrderPaymentMethod, OrderStatus
from datetime import datetime

from app.schemas.category import CategoryOut


class ProductBase(BaseModel):
    name: str
    category_id: UUID
    price: Decimal
    online_shop: bool
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductFullInfoOut(ProductBase):
    id: UUID
    active: bool
    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    id: UUID
    name: str
    price: Decimal
    online_shop: bool
    category: CategoryOut
    image_url: Union[str, None] = None
    model_config = {"from_attributes": True}


class ProductOrderOut(BaseModel):
    product_order_id: UUID
    count: int
    product_id: UUID
    product_name: str
    product_price: Decimal
    model_config = {"from_attributes": True}


class ProductShiftOrder(BaseModel):
    product_name: str
    count: int
    product_price: Decimal
    product_category: str

    order_id: UUID
    order_date: datetime
    order_price: Decimal
    order_discount: Decimal
    order_payment_method: OrderPaymentMethod
    order_type: OrderType
    order_status: OrderStatus
    debit: bool

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime(
                "%Y-%m-%dT%H:%M:%S.{:03d}Z".format(int(dt.microsecond / 1000))
            )
        },
        from_attributes=True,
    )
