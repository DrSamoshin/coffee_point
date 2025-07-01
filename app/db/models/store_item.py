import uuid
from sqlalchemy import Column, UUID, ForeignKey, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class StoreItem(Base):
    __tablename__ = "store_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    price_per_item = Column(Numeric(10, 2), nullable=True)
    date = Column(DateTime, nullable=False)
    debit = Column(Boolean, default=False)
    supply_id = Column(UUID(as_uuid=True), ForeignKey("supplies.id"), nullable=True)
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)

    item = relationship("Item", backref="store_items", lazy="joined")
    supply = relationship("Supply", backref="store_items", lazy="joined")
    shift = relationship("Shift", backref="store_items", lazy="joined")

    def __repr__(self):
        return (f"id={self.id} item_id={self.item_id} supply_id={self.supply_id} amount={self.amount}"
                f"price_per_item={self.price_per_item} debit={self.debit}")