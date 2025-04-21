import uuid

from sqlalchemy import Column, String, UUID, Boolean
from app.db.models.base_class import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    active = Column(Boolean, default=True)