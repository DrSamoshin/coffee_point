import uuid
from sqlalchemy import Column, DateTime, ForeignKey, UUID, Boolean
from sqlalchemy.orm import relationship
from app.db.base_classes import Base


class Supply(Base):
    __tablename__ = "supplies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    active = Column(Boolean, default=True)

    supplier = relationship("Supplier", backref="supplies", lazy="joined")

    def __repr__(self):
        return f"id={self.id} date={self.date} supplier_id={self.supplier_id} active={self.active}"
