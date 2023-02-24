from datetime import datetime
from typing import Optional, List
from .models import Tag

from pydantic import BaseModel, Field, AnyUrl, validator


class TagBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    class Meta:
        orm_model = Tag


class ImageBase(BaseModel):
    label: str = Field(default_factory=datetime.now)
    enable_detection: bool = False

    @validator("label", pre=True)
    def generate_label(cls, label):
        if not label:
            return str(datetime.now())
        return label


class ImageURLInput(ImageBase):
    label: Optional[str]
    url: Optional[AnyUrl]


class ImageDBInput(ImageBase):
    content_type: Optional[str] = None
    download_url: AnyUrl
    tags: List[TagBase] = []


class ImageOutput(ImageDBInput):
    id: int

    class Config:
        orm_mode = True
