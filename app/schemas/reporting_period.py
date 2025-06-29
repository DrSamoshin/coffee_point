from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReportingPeriodBase(BaseModel):
    pass

class ReportingPeriodOut(ReportingPeriodBase):
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
