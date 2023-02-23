import pprint

from .config import settings

from tempfile import SpooledTemporaryFile
import requests
from fastapi import HTTPException
from typing import Union, Tuple, List
from pydantic import SecretStr


class ImaggaClient:
    def __init__(self,
                 url: str = settings.imagga_url,
                 key: str = settings.imagga_user,
                 password: Union[str, SecretStr] = settings.imagga_secret):

        self.url = url

        self.key = key

        self.password = password

    @property
    def auth(self) -> Tuple[str, str]:
        """
        Generates authentication tuple for Imagga
        :return:
        """
        return self.key, self.password.get_secret_value()

    @staticmethod
    def _process_request(request: requests.Response) -> List[str]:
        """
        Handles errors and processes the returned JSON into a usable list of high-confidence tags
        :param request:
        :return:
        """
        # Check for status code and type
        code_group = request.status_code // 100
        request_data = request.json()

        if code_group == 5:
            raise HTTPException(503,
                                detail=f"The Imagga servers are currently unavailable with a status code of {request.status_code}. Please try again later.")
        elif code_group == 4:
            raise HTTPException(request.status_code,
                                detail="The Imagga service threw an error with the following information: "
                                       f"{request_data['status']['text']}")

        tags = list()

        for tag in request_data["result"]["tags"]:
            if tag["confidence"] > settings.confidence_threshold:
                tags.append(tag["tag"]["en"])

        return tags

    def tag_file_upload(self, file: SpooledTemporaryFile) -> List[str]:
        """Sends a POST request to the tags endpoint to perform object classification on an uploaded file.

        :param file: A file loaded into memory
        :return:
        """
        request = requests.post(settings.imagga_url,
                                auth=self.auth,
                                files={'image': file},)

        return self._process_request(request)

    def tag_url(self, image_url: str) -> List[str]:
        """Sends a GET request to the tags endpoint to perform object classification on an image hosted at the given URL

        :param image_url: URL to the image to be processed
        :return:
        """
        request = requests.get(f"{self.url}?image_url={image_url}",
                               auth=self.auth,)

        return self._process_request(request)

