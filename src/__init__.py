from os import makedirs
from flask import Flask


def init_route(app):
    from .views import users

    app.register_blueprint(users.bp)


def create_app(test_config=None):
    app = Flask(__name__)
    print(test_config)
    if test_config:
        app.config.from_mapping(test_config)

    init_route(app)
    return app
