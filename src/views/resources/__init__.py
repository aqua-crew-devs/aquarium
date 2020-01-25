from flask_restful import Api

from .channels import ChannelsResource


def init_resources(app):
    api = Api(app)

    api.add_resource(ChannelsResource, "/channels")

