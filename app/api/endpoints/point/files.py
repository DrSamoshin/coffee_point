from fastapi import APIRouter, Depends, UploadFile, File
from app.crud import files as crud_files
from app.schemas.files import ImageDelete
from app.services.authentication import get_user_id_from_token


router = APIRouter(prefix="/files", tags=["files"])


@router.get("/")
async def get_image_urls(user_id: str = Depends(get_user_id_from_token)):
    urls = await crud_files.get_image_urls()
    return {"urls": urls}


@router.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...), user_id: str = Depends(get_user_id_from_token)
):
    url = await crud_files.upload_image(file)
    return {"url": url}


@router.post("/delete/")
async def delete_image(
    request: ImageDelete, user_id: str = Depends(get_user_id_from_token)
):
    image_name = await crud_files.delete_image(request.image_url)
    return {"image_name": image_name}
