import logging
import io
import os
import uuid
from fastapi import UploadFile
from google.cloud import storage
from google.cloud.client import Client
from PIL import Image


GCS_BUCKET_NAME = "coffee_point_storage"

def get_google_client() -> Client:
    file_path = ".secrets/sa-coffee-point-crm.json"
    if os.path.exists(file_path):
        client = storage.Client.from_service_account_json(file_path)
    else:
        client = storage.Client()
    return client


async def get_image_urls():
    logging.info(f"call method get_image_urls")
    try:
        bucket = get_google_client().bucket(GCS_BUCKET_NAME)
        blobs = bucket.list_blobs()
        urls = []
        for blob in blobs:
            urls.append(blob.public_url)
    except Exception as error:
        logging.error(str(error))
    else:
        logging.info(f"urls: {len(urls)}")
        return urls

async def upload_image(file: UploadFile):
    logging.info(f"call method upload_image")
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")
        image = image.resize((512, 512))

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        filename = f"{uuid.uuid4()}.jpg"

        bucket = get_google_client().bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_file(buffer, content_type="image/jpeg")
        url = blob.public_url
    except Exception as error:
        logging.error(str(error))
    else:
        logging.info(f"image is uploaded: {url}")
        return url

async def delete_image(image_url: str):
    logging.info(f"call method delete_image")
    try:
        image_name = image_url.split('/')[-1]
        bucket = GCS_CLIENT.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(image_name)
        blob.delete()
    except Exception as error:
        logging.error(str(error))
    else:
        logging.info(f"image is deleted: {image_name}")
        return image_name