from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class StoreItemBase(BaseModel):
    item_id: UUID
    amount: Decimal
    price_per_item: Optional[Decimal] = None


class StoreItemCreate(StoreItemBase):
    supply_id: Optional[UUID] = None


class StoreItemUpdate(StoreItemBase):
    supply_id: Optional[UUID] = None


class CalculationStoreItemOut(BaseModel):
    item_id: UUID
    amount: Decimal
    item_name: str


class StoreItemOut(StoreItemBase):
    id: UUID
    item_name: Optional[str] = None
    shift_id: UUID
    date: datetime
    debit: bool
    supply_id: Optional[UUID] = None
    supplier: Optional[str] = None

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
