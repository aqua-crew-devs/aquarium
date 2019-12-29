from os import makedirs
from flask import Flask


def create_app(test_config):
    app = Flask(__name__, instance_path="/aquarium")
    if test_config:
        app.config.from_mapping(test_config)
    makedirs(app.instance_path, exist_ok=True)
    return app
