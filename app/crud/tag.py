from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Tag
from app.schemas.tag import TagCreate, TagUpdate

def get_tag(db: Session, tag_id: UUID):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tags(db: Session):
    return db.query(Tag).filter(Tag.active == True).all()

def get_deactivated_tags(db: Session):
    return db.query(Tag).filter(Tag.active == False).all()

def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, db_tag: Tag, updates: TagUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_tag, field, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def deactivate_tag(db: Session, db_tag: Tag):
    db_tag.active = False
    db.commit()
    db.refresh(db_tag)

def activate_tag(db: Session, tag_id: UUID):
    db_tag = db.query(Tag).filter(Tag.id == tag_id, Tag.active == False).first()
    if db_tag:
        db_tag.active = True
        db.commit()
        db.refresh(db_tag)
    return db_tag
