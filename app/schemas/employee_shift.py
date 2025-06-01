from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class EmployeeShiftBase(BaseModel):
    start_time: datetime
    employee_id: UUID
    shift_id: Optional[UUID]

class EmployeeShiftCreate(EmployeeShiftBase):
    pass

class EmployeeShiftUpdate(BaseModel):
    last_employee_shift: bool = False
    end_time: datetime

class EmployeeShiftOut(EmployeeShiftBase):
    id: UUID
    end_time: Optional[datetime]
    active: bool

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        },
        from_attributes=True
    )
