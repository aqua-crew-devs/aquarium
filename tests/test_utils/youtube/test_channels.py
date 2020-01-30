import json
import datetime
import os

from src.utils.youtube.channels import Channels


def test_list_channels_should_return_right_url():
    channel_req = Channels("snippet", "channel_id")

    assert channel_req.get_url() == "https://www.googleapis.com/youtube/v3/channels"


def test_list_channels_should_return_right_parameters():
    channel_req = Channels("snippet", "channel_id")

    assert channel_req.get_parameters() == {"part": "snippet", "id": "channel_id"}


def test_list_channel_should_parse_snippet_correctly():
    channel_req = Channels("snippet", "channel_id")
    with open("tests/samples/aqua_snippet.json", "r", encoding="utf-8") as f:
        sample = json.load(f)
        res = channel_req.parse_item(sample)
        assert res.id == "UC1opHUrw8rvnsadT-iGp7Cg"
        assert res.title == "Aqua Ch. 湊あくあ"
        assert (
            res.description
            == "バーチャルメイド⚓️湊あくあ(みなとあくあ)です！ど、ドジとか言わないでください！\n放送で色んな変わったゲームや雑談をしています…！！\n【生放送】#湊あくあ生放送【関連ツイート】#湊あくあ 【ファン】 #あくあクルー【絵文字】⚓️【ﾌｧﾝｱｰﾄ】 #あくあーと ※動画やﾂｲｰﾄで使用させて頂くことがあります。担当絵師：がおう先生【@umaiyo_puyoman】"
        )
        assert res.published_at == datetime.datetime(2018, 8, 1, 6, 38, 45)
        assert (
            res.thumbnail.default
            == "https://yt3.ggpht.com/a/AGF-l79lFypl4LxY5kf60UpCL6gakgSGHtN-t8hq1g=s88-c-k-c0xffffffff-no-rj-mo"
        )
        assert (
            res.thumbnail.medium
            == "https://yt3.ggpht.com/a/AGF-l79lFypl4LxY5kf60UpCL6gakgSGHtN-t8hq1g=s240-c-k-c0xffffffff-no-rj-mo"
        )
        assert (
            res.thumbnail.high
            == "https://yt3.ggpht.com/a/AGF-l79lFypl4LxY5kf60UpCL6gakgSGHtN-t8hq1g=s800-c-k-c0xffffffff-no-rj-mo"
        )
        assert res.country == "JP"

