import uuid
from sqlalchemy import Column, DateTime, UUID, Boolean
from app.db.models.base_class import Base


class ReportingPeriod(Base):
    __tablename__ = "reporting_periods"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f"id={self.id} start_time={self.start_time} end_time={self.end_time} active={self.active}"