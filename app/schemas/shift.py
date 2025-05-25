from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ShiftBase(BaseModel):
    start_time: datetime
    end_time: datetime
    employee_id: UUID

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        }
    )

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(ShiftBase):
    pass

class ShiftOut(ShiftBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}