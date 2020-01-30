from datetime import datetime

from src.models.channel import Channel
from src.controllers.channel import ChannelController


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
