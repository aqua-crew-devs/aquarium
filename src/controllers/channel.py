from src.models.channel import Channel, ChannelManager


class ChannelController:
    @staticmethod
    def get_all_channels():
        return ChannelManager.get_channels()

    @staticmethod
    def create_channel(channel: Channel):
        pass

    @staticmethod
    def get_channel(id: str) -> Channel:
        pass

    @staticmethod
    def delete_channel(id: str):
        pass
