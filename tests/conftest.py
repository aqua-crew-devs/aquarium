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


@pytest.fixture
def cli_runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client, mocker):
        self._client = client
        self._mocker = mocker

    def login(self):
        self._mocker.patch(
            "src.views.users.AuthenticationController.verify_user", return_value=True
        )
        return self._client.post(
            "/users/login", json={"username": "helloworld", "password": "pwd"}
        )


@pytest.fixture
def auth(client, app, mocker):
    with app.app_context():
        yield AuthActions(client, mocker)
