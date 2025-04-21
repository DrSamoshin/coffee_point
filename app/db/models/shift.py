import uuid
from sqlalchemy import Column, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)

    employee = relationship("Employee", back_populates="shifts")