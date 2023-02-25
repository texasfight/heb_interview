from pydantic import BaseSettings, SecretStr, PostgresDsn, AnyUrl, HttpUrl
from pathlib import Path


class ImageAPISettings(BaseSettings):
    postgres_host: str
    postgres_password: str
    postgres_user: str
    postgres_db: str
    imagga_user: str
    imagga_secret: SecretStr
    imagga_url: HttpUrl
    confidence_threshold: int = 50
    s3_url: AnyUrl = "http://localhost:9000/"
    s3_access_key: str
    s3_secret_key: SecretStr
    s3_bucket: str = "heb-images"

    @property
    def postgres_string(self):
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"

    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        env_file_encoding = "utf-8"


settings = ImageAPISettings()
