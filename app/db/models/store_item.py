import uuid
from sqlalchemy import Column, UUID, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class StoreItem(Base):
    __tablename__ = "store_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    supply_id = Column(UUID(as_uuid=True), ForeignKey("supplies.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    price_per_item = Column(Numeric(10, 2), nullable=False)

    item = relationship("Item", backref="store_items", lazy="joined")
    supply = relationship("Supply", backref="store_items", lazy="joined")
