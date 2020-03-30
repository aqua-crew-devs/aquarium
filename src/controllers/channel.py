from typing import Optional

from src.models.channel import Channel
from .exceptions import ChannelExistedException, ChannelNotExistException


class ChannelController:
    @staticmethod
    def get_all_channels():
        return Channel.get_all_channels()

    @staticmethod
    def create_channel(channel: Channel):
        if ChannelController.is_channel_existed(channel.id):
            raise ChannelExistedException(channel.id)
        channel.save()

    @staticmethod
    def get_channel(id: str) -> Optional[Channel]:
        return Channel.get_channel_by_id(id)

    @staticmethod
    def delete_channel(id: str):
        if not ChannelController.is_channel_existed(id):
            raise ChannelNotExistException(id)
        Channel.delete_by_id(id)

    @staticmethod
    def is_channel_existed(channel_id) -> bool:
        return Channel.get_channel_by_id(channel_id) is not None
