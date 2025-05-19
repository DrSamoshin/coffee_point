import uuid
from sqlalchemy import Column, ForeignKey, String, Numeric, Boolean, UUID
from sqlalchemy.orm import relationship
from app.db.models.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    active = Column(Boolean, default=True)
    online_shop = Column(Boolean, default=False)
    image_url = Column(String, nullable=True)

    category = relationship("Category", backref="products", lazy="joined")