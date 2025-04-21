import uuid
from sqlalchemy import Column, DateTime, ForeignKey, UUID, Boolean
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base


class Supply(Base):
    __tablename__ = "supplies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=False)
    active = Column(Boolean, default=True)

    supplier = relationship("Supplier", backref="supplies", lazy="joined")