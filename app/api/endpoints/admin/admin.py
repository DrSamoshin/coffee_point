import io
import logging
import pandas as pd
from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.db_sessions import get_point_db
from app.db.models import Product, Category


router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/import-products/")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_point_db)):
    logging.info(f"call method import_products")
    try:
        print(file)
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))

        df["id"] = df["id"].apply(lambda x: UUID(x))
        df["category_id"] = df["category_id"].apply(lambda x: UUID(x))
        df["price"] = df["price"].astype(float)
        df["active"] = df["active"].astype(str).str.lower() == "true"
        df["online_shop"] = df["online_shop"].astype(str).str.lower() == "true"
        df["image_url"] = df["image_url"].fillna("")

        for _, row in df.iterrows():
            product = Product(
                id=row["id"],
                name=row["name"],
                category_id=row["category_id"],
                price=row["price"],
                active=row["active"],
                online_shop=row["online_shop"],
                image_url=row["image_url"]
            )
            db.add(product)
        db.commit()
        logging.info(f"Products are imported: {len(df)}")
        return {"message": f"Imported {len(df)} products"}

    except Exception as e:
        db.rollback()
        logging.info(f"Products are not imported. error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")


@router.post("/import-categories/")
async def import_categories(file: UploadFile = File(...), db: Session = Depends(get_point_db)):
    logging.info(f"call method import_categories")
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))

        df["id"] = df["id"].apply(lambda x: UUID(x))
        df["active"] = df["active"].astype(str).str.lower() == "true"

        for _, row in df.iterrows():
            category = Category(
                id=row["id"],
                name=row["name"],
                active=row["active"]
            )
            db.add(category)
        db.commit()
        logging.info(f"categories are imported: {len(df)}")
        return {"message": f"Imported {len(df)} categories"}
    except Exception as e:
        logging.info(f"categories are not imported. error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")
