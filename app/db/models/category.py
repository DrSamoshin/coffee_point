import uuid
from sqlalchemy import Column, String, UUID, Boolean
from app.db.base_classes import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f"id={self.id} name={self.name} active={self.active}"
