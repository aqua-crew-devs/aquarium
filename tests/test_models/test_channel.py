from datetime import datetime

import pymongo
import mongomock

from src.models.channel import ChannelManager, Channel

TEST_MONGO_SERVER = ("localhost", 27017)
TEST_MONGO_SERVERS = (TEST_MONGO_SERVER,)


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_create_a_channel_if_no_such_channel_is_presented(app):
    with app.app_context():
        ChannelManager.save(
            Channel(
                **{
                    "id": "abcd",
                    "name": "helloworld",
                    "description": "an awesome channel",
                    "thumbnail": "https://url_to_thumbnails",
                    "published_at": datetime(2020, 1, 24, 6, 14, 00),
                    "country": "JP",
                }
            )
        )

        channels = pymongo.MongoClient(*TEST_MONGO_SERVER).aquarium.channels
        channel = channels.find_one({"id": "abcd"})
        assert channel is not None
        assert channel["id"] == "abcd"
        assert channel["name"] == "helloworld"
        assert channel["description"] == "an awesome channel"
        assert channel["thumbnail"] == "https://url_to_thumbnails"
        assert channel["published_at"] == datetime(2020, 1, 24, 6, 14, 00)
        assert channel["country"] == "JP"


def test_it_should_update_channel_if_channel_is_presented(app):
    with app.app_context():
        channels = pymongo.MongoClient(*TEST_MONGO_SERVER).aquarium.channels
        channels.insert_one(
            {
                "id": "abcd",
                "name": "helloworld",
                "description": "an awesome channel",
                "thumbnail": "https://url_to_thumbnails",
                "published_at": datetime(2020, 1, 24, 6, 14, 00),
                "country": "JP",
            }
        )

        ChannelManager.save(
            Channel(
                **{
                    "id": "abcd",
                    "name": "new channel name",
                    "description": "an awesome channel",
                    "thumbnail": "https://url_to_thumbnails",
                    "published_at": datetime(2020, 1, 24, 6, 14, 00),
                    "country": "JP",
                }
            )
        )

        channel = channels.find_one({"id": "abcd"})
        assert channel is not None
        assert channel["id"] == "abcd"
        assert channel["name"] == "new channel name"
