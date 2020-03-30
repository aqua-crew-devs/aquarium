from typing import Optional

from src.models.channel import Channel
from .exceptions import ChannelExistedException, ChannelNotExistException


class ChannelController:
    @staticmethod
    def get_all_channels():
        return Channel.get_all_channels()

    @staticmethod
    def create_channel(channel: Channel):
        if Channel.get_channel_by_id(channel.id) is not None:
            raise ChannelExistedException(channel.id)
        channel.save()

    @staticmethod
    def get_channel(id: str) -> Optional[Channel]:
        res = Channel.get_channel_by_id(id)
        return res

    @staticmethod
    def delete_channel(id: str):
        if Channel.get_channel_by_id(id) is None:
            raise ChannelNotExistException(id)
        Channel.delete_by_id(id)
