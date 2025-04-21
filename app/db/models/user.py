import uuid
from sqlalchemy import Column, String, Boolean, UUID
from app.db.models.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    active = Column(Boolean, default=True)
