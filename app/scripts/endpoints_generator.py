from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
target_dir = f"{BASE_DIR}/api/endpoints"

endpoints_to_create = [
    "category",
    "client",
    "item",
    "order",
    "product",
    "product_order",
    "product_tag",
    "recipe_item",
    "store_item",
    "supplier",
    "supply",
    "tag"
]

def generate_endpoint_code(entity: str) -> str:
    class_name = ''.join(word.capitalize() for word in entity.split('_'))
    return f"""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.{entity} import {class_name}Create, {class_name}Out, {class_name}Update
from app.crud import {entity} as crud_{entity}
from app.core.responses import response

# router = APIRouter(prefix='/{entity}s', tags=['{entity}s'])

@router.get("/", response_model=list[{class_name}Out])
def read_{entity}(db: Session = Depends(get_db)):
    return crud_{entity}.get_{entity}(db)

@router.get("/{{{entity}_id}}", response_model={class_name}Out)
def read_{entity}({entity}_id: UUID, db: Session = Depends(get_db)):
    db_{entity} = crud_{entity}.get_{entity}(db, {entity}_id)
    if not db_{entity}:
        return response("{entity} not found", 404)
    return db_{entity}

@router.post("/", response_model={class_name}Out)
def create_{entity}({entity}: {class_name}Create, db: Session = Depends(get_db)):
    db_{entity} = crud_{entity}.create_{entity}(db, {entity})
    return db_{entity}

@router.put("/{{{entity}_id}}", response_model={class_name}Out)
def update_{entity}({entity}_id: UUID, {entity}_update: {class_name}Update, db: Session = Depends(get_db)):
    db_{entity} = crud_{entity}.get_{entity}(db, {entity}_id)
    if not db_{entity}:
        return response("{entity} not found", 404)
    db_{entity} = crud_{entity}.update_{entity}(db, db_{entity}, {entity}_update)
    return db_{entity}
"""

for entity in endpoints_to_create:
    file_path = f"{target_dir}/{entity}.py"
    content = generate_endpoint_code(entity)
    with open(file_path, "w") as f:
        f.write(content)

# sorted(f.name for f in target_dir.iterdir() if f.stem in endpoints_to_create)