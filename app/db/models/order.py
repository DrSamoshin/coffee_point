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
    discount = Column(Numeric(3, 0), nullable=False, default=0)
    payment_method = Column(SQLAlchemyEnum(OrderPaymentMethod), nullable=False)
    type = Column(SQLAlchemyEnum(OrderType), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(OrderStatus), nullable=False)
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)
    order_number = Column(Integer, nullable=False, default=0)
    debit = Column(Boolean, default=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)

    client = relationship("Client", backref="orders", lazy="joined")
    shift = relationship("Shift", backref="orders", lazy="joined")

    def __repr__(self):
        return (f"id={self.id} price={self.price} discount={self.discount} payment_method={self.payment_method}"
                f" type={self.type} date={self.date} status={self.status} shift_id={self.shift_id}"
                f" order_number={self.order_number} active={self.debit} client_id={self.client_id}")