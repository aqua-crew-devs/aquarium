from datetime import datetime

import pymongo
import mongomock
import pytest

from src.models.channel import ChannelManager, Channel

TEST_MONGO_SERVER = ("localhost", 27017)
TEST_MONGO_SERVERS = (TEST_MONGO_SERVER,)


def create_sample_channel():
    return {
        "id": "abcd",
        "name": "helloworld",
        "description": "an awesome channel",
        "thumbnail": "https://url_to_thumbnails",
        "published_at": datetime(2020, 1, 24, 6, 14, 00),
        "country": "JP",
    }


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_create_a_channel_if_no_such_channel_is_presented(app):
    with app.app_context():
        ChannelManager.save(Channel(**create_sample_channel()))

        channels = pymongo.MongoClient(*TEST_MONGO_SERVER).aquarium.channels
        channel = channels.find_one({"id": "abcd"})
        assert channel is not None
        assert channel["id"] == "abcd"
        assert channel["name"] == "helloworld"
        assert channel["description"] == "an awesome channel"
        assert channel["thumbnail"] == "https://url_to_thumbnails"
        assert channel["published_at"] == datetime(2020, 1, 24, 6, 14, 00)
        assert channel["country"] == "JP"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_update_channel_if_channel_is_presented(app):
    with app.app_context():
        channels = pymongo.MongoClient(*TEST_MONGO_SERVER).aquarium.channels
        channels.insert_one(create_sample_channel())

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

        assert channels.count_documents({"id": "abcd"}) == 1
        channel = channels.find_one({"id": "abcd"})
        assert channel is not None
        assert channel["id"] == "abcd"
        assert channel["name"] == "new channel name"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_list_of_all_channels(app):
    with app.app_context():
        channels = pymongo.MongoClient(*TEST_MONGO_SERVER).aquarium.channels
        sample_1 = create_sample_channel()
        sample_2 = create_sample_channel()
        sample_1["id"] = "abcd"
        sample_2["id"] = "cdef"

        channels.insert_many([sample_1, sample_2])

        res = ChannelManager.get_channels()

        assert res[0].id == "abcd"
        assert res[1].id == "cdef"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_get_channel_by_id(app):
    with app.app_context():
        channels = pymongo.MongoClient(*TEST_MONGO_SERVER).aquarium.channels
        channels.insert_one(create_sample_channel())

        channel = ChannelManager.get_channel_by_id("abcd")
        assert channel is not None
        assert channel.id == "abcd"
        assert channel.name == "helloworld"
        assert channel.description == "an awesome channel"
        assert channel.thumbnail == "https://url_to_thumbnails"
        assert channel.published_at == datetime(2020, 1, 24, 6, 14, 00)
        assert channel.country == "JP"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_raise_error_if_no_such_channel_exist(app):
    with app.app_context():
        with pytest.raises(RuntimeError):
            ChannelManager.get_channel_by_id("abcd")
