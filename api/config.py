from pydantic import BaseSettings, SecretStr, PostgresDsn, AnyUrl, HttpUrl
from pathlib import Path


class ImageAPISettings(BaseSettings):
    postgres_string: PostgresDsn
    imagga_user: str
    imagga_secret: SecretStr
    imagga_url: HttpUrl
    confidence_threshold: int = 50
    s3_url: AnyUrl = "http://localhost:9444/"
    s3_access_key: str
    s3_secret_key: SecretStr
    s3_bucket: str = "heb-images"


    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        env_file_encoding = "utf-8"


settings = ImageAPISettings()

