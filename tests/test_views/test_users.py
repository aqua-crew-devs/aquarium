from unittest.mock import create_autospec

import flask


def test_it_should_login_user(app, mocker):
    mocker.patch(
        "src.views.users.AuthenticationController.verify_user", return_value=True
    )
    mocker.patch(
        "src.views.users.AuthenticationController.issue_token", return_value="token"
    )

    with app.test_client() as client:
        resp = client.post(
            "/users/login",
            json={"username": "fake_username", "password": "fake_password"},
        )
        assert resp.status_code == 200
        assert flask.session["access_token"] == "token"


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

