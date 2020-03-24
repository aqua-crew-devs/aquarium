from datetime import datetime
from unittest.mock import Mock
import json

from src.models.channel import Channel


def test_it_should_create_a_channel_in_auto_mode(client, mocker, auth):
    create_channel_mocker = mocker.patch(
        "src.views.resources.channels.ChannelController.create_channel"
    )
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
    create_channel_mocker.assert_called_with(
        Channel(
            **{
                "id": "UC1opHUrw8rvnsadT-iGp7Cg",
                "name": "Aqua Ch. 湊あくあ",
                "description": "バーチャルメイド⚓️湊あくあ(みなとあくあ)です！ど、ドジとか言わないでください！\n放送で色んな変わったゲームや雑談をしています…！！\n【生放送】#湊あくあ生放送【関連ツイート】#湊あくあ 【ファン】 #あくあクルー【絵文字】⚓️【ﾌｧﾝｱｰﾄ】 #あくあーと ※動画やﾂｲｰﾄで使用させて頂くことがあります。担当絵師：がおう先生【@umaiyo_puyoman】",
                "published_at": datetime(2018, 8, 1, 6, 38, 45),
                "thumbnail": "https://yt3.ggpht.com/a/AATXAJwHPp_TkvcWJyblt9XVYDjNSjrj6KdpQSCQNQ=s800-c-k-c0xffffffff-no-rj-mo",
                "country": "JP",
            }
        )
    )


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
