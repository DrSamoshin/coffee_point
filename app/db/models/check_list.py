import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy import Enum as SQLAlchemyEnum
from app.db.base_classes import Base
from app.core.consts import CheckListTimePoint


class CheckList(Base):
    __tablename__ = "check_lists"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    time_point = Column(SQLAlchemyEnum(CheckListTimePoint), nullable=False, unique=True)
    check_list = Column(String, nullable=True)

    def __repr__(self):
        return f"id={self.id} time_point={self.time_point} check_list={self.check_list}"
