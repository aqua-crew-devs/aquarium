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
