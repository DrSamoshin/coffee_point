import uuid
from sqlalchemy import Column, ForeignKey, DateTime, UUID, Boolean
from sqlalchemy.orm import relationship
from app.db.base_classes import Base


class EmployeeShift(Base):
    __tablename__ = "employee_shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)
    active = Column(Boolean, default=True)

    employee = relationship("Employee", backref="employee_shifts", lazy="joined")
    shift = relationship("Shift", backref="employee_shifts", lazy="joined")

    def __repr__(self):
        return (
            f"id={self.id} start_time={self.start_time} end_time={self.end_time} "
            f"employee_id={self.employee_id} employee_name={self.employee.name} shift={self.shift}"
        )
