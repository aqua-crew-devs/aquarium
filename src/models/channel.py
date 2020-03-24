from datetime import datetime
from .database import get_mongo_client


class Channel:
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        thumbnail: str,
        published_at: datetime,
        country: str,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.description = description
        self.thumbnail = thumbnail
        self.published_at = published_at
        self.country = country

    def __eq__(self, other):
        return vars(self) == vars(other)

    def serialize(self):
        res = vars(self)
        res["published_at"] = res["published_at"].strftime("%Y-%m-%d")
        return res


class ChannelManager:
    @staticmethod
    def save(channel: Channel):
        channels = get_mongo_client().aquarium.channels

        channels.find_one_and_replace({"id": channel.id}, vars(channel), upsert=True)

    @staticmethod
    def get_channels():
        channels = get_mongo_client().aquarium.channels.find()

        res = list(map(lambda channel: Channel(**channel), channels))
        return res

    @staticmethod
    def get_channel_by_id(channel_id: str) -> Channel:
        channel = get_mongo_client().aquarium.channels.find_one({"id": channel_id})
        if channel is None:
            return None
        return Channel(**channel)

    @staticmethod
    def delete_channel_by_id(channel_id: str):
        res = get_mongo_client().aquarium.channels.delete_one({"id": channel_id})

        if res.deleted_count == 0:
            raise RuntimeError("No such channel %s", channel_id)
