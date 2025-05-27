import uuid
from sqlalchemy import Column, ForeignKey, DateTime, UUID, Boolean
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    active = Column(Boolean, default=True)

    employee = relationship("Employee", backref="shifts", lazy="joined")

    def __repr__(self):
        return (f"id={self.id} start_time={self.start_time} end_time={self.end_time} "
                f"employee_id={self.employee_id} employee_name={self.employee.name}")