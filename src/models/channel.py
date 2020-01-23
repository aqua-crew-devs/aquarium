from datetime import datetime
from .database import get_mongo_client

class Channel:
    def __init__(self, id: str, name: str, description: str, thumbnail: str, published_at: datetime, country: str):
        self.id = id
        self.name = name
        self.description=description
        self.thumbnail=thumbnail
        self.published_at=published_at
        self.country=country

    def __eq__(self, other):
        return vars(self) == vars(other)

class ChannelManager:
    @staticmethod
    def save(channel: Channel):
        channels = get_mongo_client().aquarium.channels
        
        channels.insert_one(vars(channel))