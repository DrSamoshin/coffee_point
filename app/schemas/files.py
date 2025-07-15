from pydantic import BaseModel


class ImageDelete(BaseModel):
    image_url: str
