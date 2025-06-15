import uuid
from sqlalchemy import Column, String, Boolean, UUID
from app.db.models.base_class import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    deactivated = Column(Boolean, default=False)

    def __repr__(self):
        return f"id={self.id} name={self.name} deactivated={self.deactivated}"