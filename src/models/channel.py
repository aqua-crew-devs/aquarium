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


class ChannelManager:
    @staticmethod
    def save(channel: Channel):
        channels = get_mongo_client().aquarium.channels

        channels.find_one_and_replace({"id": channel.id}, vars(channel), upsert=True)

    def get_channels():
        channels = get_mongo_client().aquarium.channels.find()

        res = list(map(lambda channel: Channel(**channel), channels))
        return res
