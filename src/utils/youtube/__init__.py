import abc
import logging

import requests

from .channels import Channels
from .interface import IAPIObject


class YouTubeDataAPIResponse:
    def __init__(self, etag: str, items):
        self.etag = etag
        self.items = items


class YouTubeDataAPI:
    def __init__(self, api_key: str):
        if api_key is None or api_key == "":
            logging.getLogger("youtube").warning(
                "API key for youtube API is not set or set to empty string. Are you forgetting to set api key?"
            )
        self._api_key = api_key

    def request(self, api_object: IAPIObject):
        params = {"key": self._api_key}
        api_params = api_object.get_parameters()
        params.update(api_params)
        resp = requests.get(
            api_object.get_url(),
            params=params,
            headers={"Content-Type": "application/json"},
        )

        result = resp.json()
        return YouTubeDataAPIResponse(
            result["etag"], list(map(api_object.parse_item, result["items"]))
        )

    def get_channel_by_id(self, channel_id: str):
        return self.request(Channels("snippet", channel_id)).items
