import uuid
from sqlalchemy import Column, String, UUID, Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
from app.db.base_classes import Base
from app.core.consts import EmployeePosition


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    position = Column(SQLAlchemyEnum(EmployeePosition), nullable=False)
    deactivated = Column(Boolean, default=False)

    def __repr__(self):
        return f"id={self.id} name={self.name} position={self.position} deactivated={self.deactivated}"
