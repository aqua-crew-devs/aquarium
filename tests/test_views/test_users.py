from unittest.mock import create_autospec
from freezegun import freeze_time
import pytest

import flask


def test_it_should_login_user(app, mocker):
    mocker.patch(
        "src.views.users.AuthenticationController.verify_user", return_value=True
    )

    with app.test_client() as client:
        resp = client.post(
            "/users/login",
            json={"username": "fake_username", "password": "fake_password"},
        )
        assert resp.status_code == 200
        assert flask.session["access_token"] is not None


def test_it_should_not_login_user_if_user_verification_does_not_passed(client, mocker):
    mocker.patch(
        "src.views.users.AuthenticationController.verify_user", return_value=False
    )

    resp = client.post(
        "/users/login", json={"username": "fake_username", "password": "fake_password"},
    )
    assert resp.status_code == 403


def test_it_should_invalidate_token_when_user_logout(app):
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["access_token"] = "a token"
        resp = client.post("/users/logout")
        assert resp.status_code == 200
        assert flask.session["access_token"] == ""


def test_it_should_add_a_user_when_invoke_add_user_command(cli_runner, mocker, app):
    add_user_mocker = mocker.patch(
        "src.views.users.AuthenticationController.add_user", return_value=False
    )

    with app.app_context():
        cli_runner.invoke(args=["add-user", "username", "password"])

        add_user_mocker.assert_called_with("username", "password")


@freeze_time("2020-01-12 12:00:00")
def test_it_should_validate_user_token_when_token_is_valid(mocker, app):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="test")
    with app.test_client() as client:
        with client.session_transaction() as session:
            # a token expired at 2020-02-01 with secret is test
            session[
                "access_token"
            ] = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiY2RlIiwiZXhwaXJlZF9hdCI6IjIwMjAtMDItMDEgMDA6MDA6MDAifQ.YMLdfJVbuJM41SzcQoTX2vMN3mAHOTFP7DIqTLogVV0"
        resp = client.post("/users/validate")
        assert resp.status_code == 200


# this token expired at 2000-02-01 00:00:00
EXPIRED_TOKEN = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiY2RlIiwiZXhwaXJlZF9hdCI6IjIwMDAtMDItMDEgMDA6MDA6MDAifQ.POL706XgASDVprILLFtFRL652RK9sA8d6VO3QltjIEM"
TOKEN_GENERATED_BY_WRONG_KEY = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiY2RlIiwiZXhwaXJlZF9hdCI6IjIwMjAtMDItMDEgMDA6MDA6MDAifQ.5MRZnSSRbmdcr9vnP2FeBSEh-ZdmiBMFFofjZW30m8g"


@freeze_time("2020-01-12 12:00:00")
@pytest.mark.parametrize("token", [[EXPIRED_TOKEN], [TOKEN_GENERATED_BY_WRONG_KEY]])
def test_it_should_invalidate_user_when_token_is_wrong(mocker, app, token):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="test")
    with app.test_client() as client:
        with client.session_transaction() as session:
            # a token expired at 2020-02-01 with secret is test
            session["access_token"] = token
        resp = client.post("/users/validate")
        assert resp.status_code == 403


def test_it_should_invalidate_user_when_no_token_is_presented(mocker, app):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="test")
    with app.test_client() as client:
        resp = client.post("/users/validate")
        assert resp.status_code == 403
