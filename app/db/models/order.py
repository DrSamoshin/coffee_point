import uuid
from sqlalchemy import Column, ForeignKey, Numeric, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base
from sqlalchemy import Enum as SQLAlchemyEnum
from app.core.consts import OrderStatus, OrderPaymentMethod, OrderType


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)
    payment_method = Column(SQLAlchemyEnum(OrderPaymentMethod), nullable=False)  # example: "cash", "card"
    type = Column(SQLAlchemyEnum(OrderType), nullable=False)  # example: "dine-in", "takeaway"
    status = Column(SQLAlchemyEnum(OrderStatus), nullable=False) # example: "waiting", "completed", "cancelled", "returned"
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)
    active = Column(Boolean, default=True)
    order_number = Column(Integer, nullable=False, default=0)

    client = relationship("Client", backref="orders", lazy="joined")
    shift = relationship("Shift", backref="orders", lazy="joined")