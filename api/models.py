from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, URL
from sqlalchemy.orm import relationship
from .database import Base


class ImageTagJunction(Base):
    __tablename__ = "image_tag_junction"

    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
    tag_name = Column(String, ForeignKey("tags.name"), primary_key=True)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String, nullable=False, index=False)
    enable_detection = Column(Boolean, nullable=False)
    content_type = Column(String, nullable=True)
    download_url = Column(String)

    tags = relationship("Tag", back_populates="images", secondary="image_tag_junction")


class Tag(Base):
    __tablename__ = "tags"

    name = Column(String, primary_key=True)

    images = relationship(
        "Image", back_populates="tags", secondary="image_tag_junction"
    )
