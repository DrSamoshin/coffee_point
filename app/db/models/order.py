import uuid
from sqlalchemy import Column, ForeignKey, String, Numeric, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base
import enum
from sqlalchemy import Enum as SQLAlchemyEnum

class PaymentMethod(enum.Enum):
    cash = "cash"
    card = "card"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)
    payment_method = Column(SQLAlchemyEnum(PaymentMethod), nullable=False)  # example: "cash", "card"
    kind = Column(String, nullable=False)  # example: "dine-in", "takeaway"
    active = Column(Boolean, default=True)

    client = relationship("Client", backref="orders", lazy="joined")