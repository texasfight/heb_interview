from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"


def parse_pydantic_schema(schema):
    """
        Iterates through pydantic schema and parses nested schemas
        to a dictionary containing SQLAlchemy models.
        Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value):
                if is_pydantic(value[0]):
                    parsed_schema[key] = [schema.Meta.orm_model(**schema.dict()) for schema in value]
            else:
                if is_pydantic(value):
                    parsed_schema[key] = value.Meta.orm_model(**value.dict())
        except AttributeError:
            raise AttributeError("Found nested Pydantic model but Meta.orm_model was not specified.")
    return parsed_schema


def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter_by(id=image_id).first()


def get_all_images(db: Session):
    return db.query(models.Image).all()


def get_images_by_tags(db: Session, tags: List[str]):
    base_query = db.query(models.Image)
    for tag in tags:
        # add another filter based on tag name for each query
        base_query = base_query.filter(models.Image.tags.any(name=tag))
    return base_query.all()


def add_image(db: Session, image: schemas.ImageDBInput) -> ...:
    parsed_schema = parse_pydantic_schema(image)
    db_image = models.Image(**parsed_schema)
    db_image = db.merge(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
