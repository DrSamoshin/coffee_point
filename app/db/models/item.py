import uuid
from sqlalchemy import Column, String, UUID, Boolean, Integer
from app.db.models.base_class import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    measurement = Column(String, nullable=False)
    lower_limit = Column(Integer, nullable=True, default=0)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f"id={self.id} name={self.name} measurement={self.measurement} active={self.active}"
