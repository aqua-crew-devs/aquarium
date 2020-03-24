from src.models.channel import Channel, ChannelManager
from .exceptions import ChannelExistedException, ChannelNotExistException


class ChannelController:
    @staticmethod
    def get_all_channels():
        return ChannelManager.get_channels()

    @staticmethod
    def create_channel(channel: Channel):
        if ChannelManager.get_channel_by_id(channel.id) is not None:
            raise ChannelExistedException(channel.id)
        channel.save(channel)

    @staticmethod
    def get_channel(id: str) -> Channel:
        res = ChannelManager.get_channel_by_id(id)
        if res is None:
            raise ChannelNotExistException(id)
        return res

    @staticmethod
    def delete_channel(id: str):
        if ChannelManager.get_channel_by_id(id) is None:
            raise ChannelNotExistException(id)
        ChannelManager.delete_channel_by_id(id)
