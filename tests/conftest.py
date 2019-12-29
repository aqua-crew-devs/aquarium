import pytest

from src import create_app


@pytest.fixture
def app():
    test_config = {"TESTING": True, "SECRET_KEY": "test"}
    app = create_app(test_config)

    return app


@pytest.fixture
def client(app):
    return app.test_client()
