from datetime import datetime

from src.models.channel import Channel


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
