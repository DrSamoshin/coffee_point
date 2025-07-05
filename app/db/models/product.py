import uuid
from sqlalchemy import Column, ForeignKey, String, Numeric, Boolean, UUID
from sqlalchemy.orm import relationship
from app.db.base_classes import Base

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

    def __repr__(self):
        return (f"id={self.id} name={self.name} category_id={self.category_id} price={self.price}"
                f" active={self.active} online_shop={self.online_shop} image_url={self.image_url}")