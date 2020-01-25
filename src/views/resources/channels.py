from flask_restful import Resource

from src.controllers.channel import ChannelController


class ChannelsResource(Resource):
    def get(self):
        channels = ChannelController.get_all_channels()
        return list(map(lambda c: c.serialize(), channels))
