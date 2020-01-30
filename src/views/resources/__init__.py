from flask_restful import Api

from .channels import ChannelsResource, ChannelsIndexResource


def init_resources(app):
    api = Api(app)

    api.add_resource(ChannelsResource, "/channels")
    api.add_resource(ChannelsIndexResource, "/channels/<id>")

