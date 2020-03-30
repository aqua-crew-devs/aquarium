from datetime import datetime
from unittest.mock import Mock
import json

import mongomock
import pymongo

from src.models.channel import Channel

TEST_MONGO_SERVER = ("localhost", 27017)
TEST_MONGO_SERVERS = (TEST_MONGO_SERVER,)


def create_sample_channel():
    return {
        "id": "UC1opHUrw8rvnsadT-iGp7Cg",
        "name": "helloworld",
        "description": "an awesome channel",
        "thumbnail": "https://url_to_thumbnails",
        "published_at": datetime(2020, 1, 24, 6, 14, 00),
        "country": "JP",
    }


def get_fake_db():
    return pymongo.MongoClient("localhost", 27017).aquarium


def get_channels_collection():
    return get_fake_db().channels


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_create_a_channel_in_auto_mode(client, mocker, auth):
    with open(
        "./tests/samples/channel_snippet_resp.json", encoding="utf-8"
    ) as json_sample:
        mocked_resp = Mock()
        mocked_resp.json = Mock(return_value=json.load(json_sample))
        mocker.patch("requests.get", return_value=mocked_resp)

        auth.login()
        resp = client.post(
            "/channels",
            json={"mode": "auto", "channel": {"id": "UC1opHUrw8rvnsadT-iGp7Cg"}},
        )

        assert resp.status_code == 201
        channel = get_channels_collection().find_one({"id": "UC1opHUrw8rvnsadT-iGp7Cg"})
        assert channel["name"] == "Aqua Ch. 湊あくあ"
        assert (
            channel["description"]
            == "バーチャルメイド⚓️湊あくあ(みなとあくあ)です！ど、ドジとか言わないでください！\n放送で色んな変わったゲームや雑談をしています…！！\n【生放送】#湊あくあ生放送【関連ツイート】#湊あくあ 【ファン】 #あくあクルー【絵文字】⚓️【ﾌｧﾝｱｰﾄ】 #あくあーと ※動画やﾂｲｰﾄで使用させて頂くことがあります。担当絵師：がおう先生【@umaiyo_puyoman】"
        )
        assert channel["published_at"] == datetime(2018, 8, 1, 6, 38, 45)
        assert (
            channel["thumbnail"]
            == "https://yt3.ggpht.com/a/AATXAJwHPp_TkvcWJyblt9XVYDjNSjrj6KdpQSCQNQ=s800-c-k-c0xffffffff-no-rj-mo"
        )
        assert channel["country"] == "JP"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_create_a_channel_in_manual_mode(client, mocker, auth):
    aqua_channel = {
        "id": "UC1opHUrw8rvnsadT-iGp7Cg",
        "name": "Aqua Ch. 湊あくあ",
        "description": "sample desp",
        "published_at": "2018-07-31",
        "thumbnail": "https://yt3.ggpht.com/a/AGF-l79lFypl4LxY5kf60UpCL6gakgSGHtN-t8hq1g=s288-c-k-c0xffffffff-no-rj-mo",
        "country": "JP",
    }

    auth.login()

    resp = client.post("/channels", json={"mode": "manual", "channel": aqua_channel,},)
    assert resp.status_code == 201
    channel = get_channels_collection().find_one({"id": "UC1opHUrw8rvnsadT-iGp7Cg"})
    assert channel["name"] == "Aqua Ch. 湊あくあ"
    assert channel["description"] == "sample desp"

    assert channel["published_at"] == datetime(2018, 7, 31, 0, 0, 0)
    assert (
        channel["thumbnail"]
        == "https://yt3.ggpht.com/a/AGF-l79lFypl4LxY5kf60UpCL6gakgSGHtN-t8hq1g=s288-c-k-c0xffffffff-no-rj-mo"
    )
    assert channel["country"] == "JP"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_return_code_1_400_error_in_auto_mode_if_no_such_channel_exist(
    client, mocker, auth
):
    create_channel_mocker = mocker.patch(
        "src.views.resources.channels.ChannelController.create_channel"
    )
    with open(
        "./tests/samples/channel_empty_resp.json", encoding="utf-8"
    ) as json_sample:
        mocked_resp = Mock()
        mocked_resp.json = Mock(return_value=json.load(json_sample))
        mocker.patch("requests.get", return_value=mocked_resp)

    auth.login()
    resp = client.post(
        "/channels",
        json={"mode": "auto", "channel": {"id": "UC1opHUrw8rvnsadT-iGp7Cg"}},
    )

    assert resp.status_code == 400
    res = resp.get_json()
    res["code"] == 1


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_return_code_2_400_error_if_there_have_such_channel_exist(
    client, app, auth
):
    with app.app_context():
        channels = get_channels_collection()
        channels.insert(create_sample_channel())

        auth.login()
        resp = client.post(
            "/channels",
            json={"mode": "auto", "channel": {"id": "UC1opHUrw8rvnsadT-iGp7Cg"}},
        )

        assert resp.status_code == 400
        res = resp.get_json()
        res["code"] == 2
