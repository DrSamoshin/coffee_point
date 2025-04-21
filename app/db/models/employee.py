import uuid
from sqlalchemy import Column, String, UUID, Boolean
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
