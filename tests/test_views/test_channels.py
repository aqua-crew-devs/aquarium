from datetime import datetime
from unittest.mock import Mock
import json

from src.models.channel import Channel
from src.controllers.exceptions import ChannelExistedException, ChannelNotExistException


def create_sample_channel():
    return {
        "id": "abcd",
        "name": "helloworld",
        "description": "an awesome channel",
        "thumbnail": "https://url_to_thumbnails",
        "published_at": datetime(2020, 1, 24, 6, 14, 00),
        "country": "JP",
    }


def test_it_should_list_all_channels(client, mocker):
    channel_1 = create_sample_channel()
    channel_2 = create_sample_channel()

    channel_1["id"] = "channel_1"
    channel_2["id"] = "channel_2"
    mocker.patch(
        "src.views.resources.channels.ChannelController.get_all_channels",
        return_value=[Channel(**channel_1), Channel(**channel_2)],
    )

    resp = client.get("/channels")
    assert resp.status_code == 200
    data = resp.json
    assert len(data) == 2
    assert data[0]["id"] == "channel_1"
    assert data[1]["id"] == "channel_2"


def test_it_should_return_400_if_request_is_not_authenticated(client):
    resp = client.post(
        "/channels",
        json={"mode": "auto", "channel": {"id": "UC1opHUrw8rvnsadT-iGp7Cg"}},
    )
    assert resp.status_code == 403


def test_it_should_return_channel(client, mocker):
    mocker.patch(
        "src.views.resources.channels.ChannelController.get_channel",
        return_value=Channel(**create_sample_channel()),
    )
    resp = client.get("/channels/abcd")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["id"] == "abcd"
    assert payload["name"] == "helloworld"
    assert payload["description"] == "an awesome channel"
    assert payload["published_at"] == "2020-01-24"
    assert payload["thumbnail"] == "https://url_to_thumbnails"
    assert payload["country"] == "JP"


def test_it_should_return_404_if_channel_not_exist(client, mocker):
    mocker.patch(
        "src.views.resources.channels.ChannelController.get_channel",
        side_effect=ChannelNotExistException("not_exist"),
    )

    resp = client.get("/channels/not_exist")
    assert resp.status_code == 404


def test_it_should_delete_a_channel(client, mocker, auth):
    auth.login()
    delete_channel = mocker.patch(
        "src.views.resources.channels.ChannelController.delete_channel"
    )

    resp = client.delete("/channels/abcd")
    delete_channel.assert_called_with("abcd")
    assert resp.status_code == 200


def test_it_should_throw_403_if_attempt_to_delete_a_channel_without_authorization(
    client,
):
    resp = client.delete("/channels/abcd")
    assert resp.status_code == 403


def test_it_should_throw_404_if_attempt_to_delete_a_channel_not_existed(
    client, mocker, auth
):
    auth.login()
    mocker.patch(
        "src.views.resources.channels.ChannelController.delete_channel",
        side_effect=ChannelNotExistException("abcd"),
    )

    resp = client.delete("/channels/abcd")
    assert resp.status_code == 404
