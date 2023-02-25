import boto3
from tempfile import SpooledTemporaryFile
from typing import Optional, Union
from io import IOBase
from urllib.parse import quote

from .config import settings


class S3_Client:
    def __init__(
        self,
        access_key: str = settings.s3_access_key,
        secret_key: str = settings.s3_secret_key.get_secret_value(),
        url: str = settings.s3_url,
        bucket: str = settings.s3_bucket,
    ):
        self.client = boto3.client(
            service_name="s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=url,
        )

        self.url = url

        self.bucket = bucket

    def upload_file(
        self,
        file_obj: Union[SpooledTemporaryFile, IOBase],
        label: str,
        bucket: Optional[str] = None,
    ) -> str:
        """

        :param file_obj: File in memory to be uploaded to the bucket
        :param label: name of the file
        :param bucket: name of the s3 bucket, defaults to provided bucket from construction
        :return: the URL to access the final files
        """
        if not bucket:
            bucket = self.bucket

        self.client.upload_fileobj(file_obj, bucket, label)

        return f"http://localhost:9000/{bucket}/{quote(label)}"
