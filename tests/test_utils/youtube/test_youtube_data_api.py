from unittest.mock import create_autospec
from src.utils.youtube import YouTubeDataAPI, IAPIObject

import requests


def test_request_data(mocker):
    response_mocker = create_autospec(requests.Response)
    response_mocker.json.return_value = {"etag": "12345", "items": [{"field_1": 1}]}
    get_mocker = mocker.patch("requests.get", return_value=response_mocker)

    class FakeAPIObject(IAPIObject):
        def get_url(self):
            return "http://helloworld.com/api"

        def get_parameters(self):
            return {"hello": 123}

        def parse_item(self, item):
            return {"alter_field_1": item["field_1"]}

    ytb_api = YouTubeDataAPI("api_key")
    resp = ytb_api.request(FakeAPIObject())

    get_mocker.assert_called_with(
        "http://helloworld.com/api",
        params={"hello": 123, "key": "api_key"},
        headers={"Content-Type": "application/json"},
    )

    assert resp.etag == "12345"
    assert len(resp.items) == 1
    assert resp.items[0]["alter_field_1"] == 1

