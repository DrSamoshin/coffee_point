from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Tag
from app.db.session import db_safe
from app.schemas.tag import TagCreate, TagUpdate

@db_safe
def get_tag(db: Session, tag_id: UUID):
    return db.query(Tag).filter(Tag.id == tag_id).first()

@db_safe
def get_tags(db: Session):
    return db.query(Tag).filter(Tag.active == True).all()

@db_safe
def get_deactivated_tags(db: Session):
    return db.query(Tag).filter(Tag.active == False).all()

@db_safe
def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@db_safe
def update_tag(db: Session, db_tag: Tag, updates: TagUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_tag, field, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@db_safe
def deactivate_tag(db: Session, db_tag: Tag):
    db_tag.active = False
    db.commit()
    db.refresh(db_tag)

@db_safe
def activate_tag(db: Session, tag_id: UUID):
    db_tag = db.query(Tag).filter(Tag.id == tag_id, Tag.active == False).first()
    if db_tag:
        db_tag.active = True
        db.commit()
        db.refresh(db_tag)
    return db_tag
