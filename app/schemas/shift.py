from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ShiftBase(BaseModel):
    pass

class ShiftCreate(ShiftBase):
    pass

class ShiftStartUpdate(BaseModel):
    # start_time: datetime
    ...

class ShiftEndUpdate(BaseModel):
    # end_time: datetime
    ...

class ShiftOut(ShiftBase):
    id: UUID
    active: bool
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        },
        from_attributes=True
    )
