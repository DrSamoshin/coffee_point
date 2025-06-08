from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.employee import EmployeeOut


class EmployeeShiftBase(BaseModel):
    employee_id: UUID
    shift_id: Optional[UUID] = None

class EmployeeShiftCreate(EmployeeShiftBase):
    pass

class EmployeeShiftUpdate(BaseModel):
    last_employee_shift: bool = False

class EmployeeShiftOut(EmployeeShiftBase):
    id: UUID
    active: bool
    start_time: datetime
    end_time: Optional[datetime] = None

    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
        json_encoders={
            datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S.{:03d}Z'.format(int(dt.microsecond / 1000)))
        },
        from_attributes=True
    )

class EmployeeShiftWithEmployeeOut(BaseModel):
    id: UUID
    employee: EmployeeOut

