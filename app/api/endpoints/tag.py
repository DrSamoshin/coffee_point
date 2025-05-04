from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.tag import TagCreate, TagOut, TagUpdate
from app.crud import tag as crud_tag
from app.core.responses import response
from app.middleware.authentication import get_user_id_from_token

router = APIRouter(prefix='/tags', tags=['tags'])

@router.get("/", response_model=list[TagOut])
def read_tags(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_tag.get_tags(db)

@router.get("/{tag_id}", response_model=TagOut)
def read_tag(tag_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_tag = crud_tag.get_tag(db, tag_id)
    if not db_tag:
        return response("tag not found", 404)
    return db_tag

@router.post("/", response_model=TagOut)
def create_tag(tag: TagCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_tag = crud_tag.create_tag(db, tag)
    return db_tag

@router.put("/{tag_id}", response_model=TagOut)
def update_tag(tag_id: UUID, tag_update: TagUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_tag = crud_tag.get_tag(db, tag_id)
    if not db_tag:
        return response("tag not found", 404)
    db_tag = crud_tag.update_tag(db, db_tag, tag_update)
    return db_tag
