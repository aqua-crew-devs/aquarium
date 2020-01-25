from os import makedirs, getenv
from flask import Flask

from .views.resources import init_resources


def init_route(app):
    from .views import users

    app.register_blueprint(users.bp)


def init_cli_command(app):
    from .views import users

    users.init_add_user(app)


def create_app(test_config=None):
    app = Flask(__name__)
    mode = getenv("MODE", "develop")

    if mode == "production":
        app.config.from_pyfile("./configs/production.py")
    elif mode == "test":
        app.config.from_pyfile("./configs/test.py")
    else:
        # mode: develop
        app.config.from_pyfile("./configs/develop.py")
    if test_config:
        app.config.from_mapping(test_config)

    init_route(app)
    init_resources(app)
    init_cli_command(app)
    return app
