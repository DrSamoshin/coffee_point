from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_classes import Base


class RecipeItem(Base):
    __tablename__ = "recipe_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    product = relationship("Product", backref="recipe_items")
    item = relationship("Item", backref="recipe_items")

    def __repr__(self):
        return f"id={self.id} product_id={self.product_id} item_id={self.item_id} amount={self.amount}"
