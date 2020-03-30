from typing import Optional, List

import deprecation

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

    def save(self):
        channels = get_mongo_client().aquarium.channels
        channels.find_one_and_replace({"id": self.id}, vars(self), upsert=True)

    @staticmethod
    def get_channel_by_id(channel_id: str) -> Optional["Channel"]:
        channel = get_mongo_client().aquarium.channels.find_one({"id": channel_id})
        if channel is None:
            return None
        return Channel(**channel)

    @staticmethod
    def get_all_channels() -> List["Channel"]:
        channels = get_mongo_client().aquarium.channels.find()
        res = list(map(lambda channel: Channel(**channel), channels))
        return res

    @staticmethod
    def delete_by_id(id: str):
        res = get_mongo_client().aquarium.channels.delete_one({"id": id})
        if res.deleted_count == 0:
            raise RuntimeError("No such channel %s", id)
