from os import makedirs
from flask import Flask


def create_app():
    app = Flask(__name__, instance_path="/aquarium")

    makedirs(app.instance_path, exist_ok=True)

    return app
