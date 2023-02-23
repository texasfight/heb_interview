from pydantic import BaseSettings, SecretStr, PostgresDsn, HttpUrl
from pathlib import Path


class ImageAPISettings(BaseSettings):
    postgres_string: PostgresDsn
    imagga_user: str
    imagga_secret: SecretStr
    imagga_url: HttpUrl
    confidence_threshold: int = 50

    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        env_file_encoding = "utf-8"


settings = ImageAPISettings()
