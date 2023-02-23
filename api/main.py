from fastapi import FastAPI, File, Form, UploadFile, Depends, HTTPException
from typing import Optional, List, Union
from sqlalchemy.orm import Session

from .schemas import ImageURLInput, ImageOutput, ImageDBInput, Tag
from .models import Base
from .database import SessionLocal, engine
from .imagga_client import ImaggaClient
from . import db_interface


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/images", response_model=List[ImageOutput])
async def get_filtered_images(objects: str = "", db: Session = Depends(get_db)):
    if not objects:
        return db_interface.get_all_images(db)

    objects = objects.strip('"')
    final_objects = objects.split(",")
    final_objects = [tag.strip() for tag in final_objects if tag]
    return db_interface.get_images_by_tags(db, final_objects)


@app.get("/images/{imageId}", response_model=ImageOutput)
async def get_image_details(image_id: int, db: Session = Depends(get_db)):
    output = db_interface.get_image(db, image_id)

    if not output:
        raise HTTPException(404, f"No image found with id: {image_id}")
    return output


@app.post("/images", response_model=ImageOutput)
async def add_image(
    file: UploadFile = File(None),
    url: str = Form(None),
    label: str = Form(None),
    enable_detection: bool = Form(False),
    db: Session = Depends(get_db),
):
    tags = list()

    if enable_detection:
        client = ImaggaClient()
        tags = client.tag_file_upload(file.file)

    image = ImageDBInput(
        label=label,
        enable_detection=enable_detection,
        tags=[Tag(name=tag) for tag in tags],
    )
    return db_interface.add_image(db, image)


@app.put("/images", response_model=ImageOutput)
async def add_image_from_url(image_input: ImageURLInput, db: Session = Depends(get_db)):
    tags = list()

    if image_input.enable_detection:
        client = ImaggaClient()
        tags = client.tag_url(image_input.url)

    image = ImageDBInput(
        **image_input.dict(include={"label", "enable_detection"}),
        tags=[Tag(name=tag) for tag in tags],
    )
    return db_interface.add_image(db, image)
