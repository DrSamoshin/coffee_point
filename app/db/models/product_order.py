from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.models.base_class import Base

class ProductOrder(Base):
    __tablename__ = "product_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    count = Column(Integer, nullable=False, default=1)

    product = relationship("Product", backref="product_orders", lazy="joined")
    order = relationship("Order", backref="product_orders", lazy="joined")