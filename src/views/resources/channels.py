from flask_restful import Resource
from flask import request, session, make_response
from dateutil.parser import parse

from src.controllers.channel import ChannelController
from src.controllers.auth import AuthenticationController
from src.controllers.exceptions import ChannelExistedException
from src.models.channel import Channel


def fetch_channel_info_from_youtube(channel_id: str) -> Channel:
    pass


class ChannelsResource(Resource):
    def get(self):
        channels = ChannelController.get_all_channels()
        return list(map(lambda c: c.serialize(), channels))

    def post(self):
        if "access_token" not in session:
            return make_response("", 403)

        if not AuthenticationController.verify_token(session["access_token"]):
            return make_response("", 403)
        payload = request.get_json()
        mode = payload["mode"]

        if mode == "manual":
            payload["channel"]["published_at"] = parse(
                payload["channel"]["published_at"]
            )
            channel = Channel(**payload["channel"])

        else:
            # mode == 'auto'
            channel_id = payload["channel"]["id"]
            channel = fetch_channel_info_from_youtube(channel_id)

        try:
            ChannelController.create_channel(channel)
        except ChannelExistedException:
            return {"code": 2}, 400

        return "", 201
