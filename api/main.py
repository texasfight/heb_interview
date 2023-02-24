from fastapi import FastAPI, File, Form, UploadFile, Depends, HTTPException
from typing import Optional, List, Union
from sqlalchemy.orm import Session
import requests
from io import BytesIO
from datetime import datetime
from copy import deepcopy

from .schemas import ImageURLInput, ImageOutput, ImageDBInput, Tag
from .models import Base
from .database import SessionLocal, engine
from .imagga_client import ImaggaClient
from . import db_interface
from .s3_client import S3_Client


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/images", response_model=List[ImageOutput])
def get_filtered_images(objects: str = "", db: Session = Depends(get_db)):
    if not objects:
        return db_interface.get_all_images(db)

    objects = objects.strip('"')
    final_objects = objects.split(",")
    final_objects = [tag.strip() for tag in final_objects if tag]
    return db_interface.get_images_by_tags(db, final_objects)


@app.get("/images/{imageId}", response_model=ImageOutput)
def get_image_details(image_id: int, db: Session = Depends(get_db)):
    output = db_interface.get_image(db, image_id)

    if not output:
        raise HTTPException(404, f"No image found with id: {image_id}")
    return output


@app.post("/images", response_model=ImageOutput)
def add_image(
    file: UploadFile = File(None),
    url: str = Form(None),
    label: str = Form(None),
    enable_detection: bool = Form(False),
    db: Session = Depends(get_db),
):
    """
    Upload an image to our psuedo-S3 bucket, optionally performs object detection, and stores in our DB

    :param file:
    :param url:
    :param label:
    :param enable_detection:
    :param db:
    :return:
    """
    if not label:
        label = str(datetime.now())

    if not url and not file:
        raise HTTPException(400, "One of `file` or `url` must be provided.")

    tags = list()

    # Handle if we got a file or URL, with focus o
    if not file:
        file_request = requests.get(url, stream=True)

        # Non 200-series response
        if file_request.status_code // 100 != 2:
            raise HTTPException(404, "Unable to query to given URL for an image.")

        file_data = BytesIO(file_request.content)
        file_type = file_request.headers['content-type']

    else:
        file_data = file.file
        file_type = file.content_type

    # Handling IO and ensuring we close the file if we get any exceptions
    try:
        if enable_detection:
            client = ImaggaClient()
            imagga_file = deepcopy(file_data)
            # BytesIO objects clear themselves after reading, so we need a copy of the file-like
            try:
                tags = client.tag_file_upload(imagga_file)
            finally:
                imagga_file.close()

        s3_client = S3_Client()

        download_url = s3_client.upload_file(file_data, label)
    finally:
        file_data.close()

    print(download_url)

    image = ImageDBInput(
        label=label,
        enable_detection=enable_detection,
        content_type=file_type,
        download_url=download_url,
        tags=[Tag(name=tag) for tag in tags],
    )
    return db_interface.add_image(db, image)


@app.put("/images", response_model=ImageOutput)
def add_image_from_url(image_input: ImageURLInput, db: Session = Depends(get_db)):
    tags = list()

    if image_input.enable_detection:
        client = ImaggaClient()
        tags = client.tag_url(image_input.url)

    image = ImageDBInput(
        **image_input.dict(include={"label", "enable_detection"}),
        tags=[Tag(name=tag) for tag in tags],
    )
    return db_interface.add_image(db, image)
