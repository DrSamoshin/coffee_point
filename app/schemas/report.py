from uuid import UUID
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.core.consts import OrderType, OrderPaymentMethod, OrderStatus


class ShiftReportCategory(BaseModel):
    category_name: str
    order_date: datetime
    count: int

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


class ShiftReportProduct(BaseModel):
    product_name: str
    category_name: str
    count: int
    products_price: Decimal


class ShiftReportOrder(BaseModel):
    order_id: UUID
    order_date: datetime
    order_price: Decimal
    order_discount: Decimal
    order_payment_method: OrderPaymentMethod
    order_type: OrderType
    order_status: OrderStatus

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


class ShiftReportOut(BaseModel):
    income: Decimal
    sold_products_count: int
    orders_count: int
    debited_orders_count: int
    average_bill: Decimal

    product_categories: list[ShiftReportCategory]
    products: list[ShiftReportProduct]
    orders: list[ShiftReportOrder]
    debited_product_categories: list[ShiftReportCategory]
    debited_products: list[ShiftReportProduct]
    debited_orders: list[ShiftReportOrder]

    model_config = {"from_attributes": True}
