from datetime import datetime

import pytest

from src.models.channel import Channel
from src.controllers.channel import ChannelController
from src.controllers.exceptions import ChannelExistedException, ChannelNotExistException


def create_sample_channel():
    return {
        "id": "abcd",
        "name": "helloworld",
        "description": "an awesome channel",
        "thumbnail": "https://url_to_thumbnails",
        "published_at": datetime(2020, 1, 24, 6, 14, 0),
        "country": "JP",
    }


def test_it_should_return_all_channels(mocker):
    channel_1 = create_sample_channel()
    channel_2 = create_sample_channel()
    channel_1["id"] = "channel_1"
    channel_2["id"] = "channel_2"
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channels",
        return_value=[Channel(**channel_1), Channel(**channel_2)],
    )

    res = ChannelController.get_all_channels()
    assert res[0] == Channel(**channel_1)
    assert res[1] == Channel(**channel_2)


def test_it_should_create_channel(mocker):
    channel = Channel(**create_sample_channel())
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channel_by_id", return_value=None,
    )
    save = mocker.patch("src.controllers.channel.Channel.save", return_value=None,)
    ChannelController.create_channel(channel)

    save.assert_called_with(channel)


def test_it_should_raise_channel_existed_exception_when_attempt_to_create_existed_channel(
    mocker,
):
    channel = Channel(**create_sample_channel())
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channel_by_id",
        return_value=Channel,
    )
    save = mocker.patch("src.controllers.channel.Channel.save", return_value=None,)

    with pytest.raises(ChannelExistedException):
        ChannelController.create_channel(channel)


def test_it_should_return_channel_by_id(mocker):
    channel = Channel(**create_sample_channel())
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channel_by_id",
        return_value=channel,
    )

    res = ChannelController.get_channel("abcd")
    assert res == channel


def test_it_should_return_None_if_try_to_get_not_existing_channel(mocker):
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channel_by_id", return_value=None,
    )
    assert ChannelController.get_channel("abcd") is None


def test_it_should_delete_channel(mocker):
    channel = Channel(**create_sample_channel())
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channel_by_id",
        return_value=channel,
    )
    delete = mocker.patch(
        "src.controllers.channel.ChannelManager.delete_channel_by_id",
    )

    ChannelController.delete_channel("abcd")
    delete.assert_called_with("abcd")


def test_it_should_raise_not_existed_channel_if_attempt_to_delete_such_one(mocker):
    channel = Channel(**create_sample_channel())
    mocker.patch(
        "src.controllers.channel.ChannelManager.get_channel_by_id", return_value=None,
    )
    delete = mocker.patch(
        "src.controllers.channel.ChannelManager.delete_channel_by_id",
    )

    with pytest.raises(ChannelNotExistException):
        ChannelController.delete_channel("abcd")
