from freezegun import freeze_time
import jwt
import pytest

from src.controllers.auth import AuthenticationController
from src.models.user import User


def test_verify_user_should_pass_when_user_provides_correct_credential(mocker):
    mocker.patch(
        "src.controllers.auth.UserManager.get_by_username",
        return_value=User(
            "fake_username",
            # generate_password_hash('fake_password')
            "pbkdf2:sha256:150000$D3ceVJbV$46c59e4a12159efb6e3c89a7e6361298ab3319199f559e8640ad07af6f21e9f4",
        ),
    )

    assert (
        AuthenticationController.verify_user("fake_username", "fake_password") == True
    )


def test_verify_user_should_reject_when_user_is_not_found(mocker):
    mocker.patch("src.controllers.auth.UserManager.get_by_username", return_value=None)

    assert (
        AuthenticationController.verify_user("fake_username", "fake_password") == False
    )


def test_verify_user_should_reject_when_password_is_wrong(mocker):
    mocker.patch(
        "src.controllers.auth.UserManager.get_by_username",
        return_value=User(
            "fake_username",
            # hash for 'true_password'
            "pbkdf2:sha256:150000$iWo0o5IB$6cd7b9ff4346d3fbaf2e7db15d24fcaacb64c9a50e09519f2e08a109adf5e0d6",
        ),
    )

    assert (
        AuthenticationController.verify_user("fake_username", "fake_password") == False
    )


@freeze_time("2019-12-29 13:53:01")
def test_issue_token_should_issue_a_token(mocker):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="secret")

    token_issued = AuthenticationController.issue_token("fake_user", 60 * 60)

    assert (
        token_issued
        == b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZha2VfdXNlciIsImV4cGlyZWRfYXQiOiIyMDE5LTEyLTI5IDE0OjUzOjAxIn0.UPwhzxzu9mNoxJKXlzS7mOysfu69lB-QkEmlkgsEirQ"
    )


@freeze_time("2019-12-29 14:11:00")
def test_verify_token_should_pass_a_valid_token(mocker):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="secret")

    assert (
        AuthenticationController.verify_token(
            b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZha2VfdXNlciIsImV4cGlyZWRfYXQiOiIyMDE5LTEyLTI5IDE1OjExOjAwIn0.W92iFKuQPab5Kos-5PAfXd7YUNt5xhnRyh0nNoUs8eM"
        )
        == True
    )


@freeze_time("2019-12-29 15:11:01")
def test_verify_token_should_reject_an_expired_token(mocker):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="secret")

    assert (
        AuthenticationController.verify_token(
            b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZha2VfdXNlciIsImV4cGlyZWRfYXQiOiIyMDE5LTEyLTI5IDE1OjExOjAwIn0.W92iFKuQPab5Kos-5PAfXd7YUNt5xhnRyh0nNoUs8eM"
        )
        == False
    )


def test_verify_token_should_reject_an_invalid_token(mocker):
    mocker.patch("src.controllers.auth.get_jwt_secret", return_value="secret")

    assert (
        AuthenticationController.verify_token(
            # generate with 'wrong_secret'
            b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZha2VfdXNlciIsImV4cGlyZWRfYXQiOiIyMDE5LTEyLTI5IDE1OjExOjAwIn0.v7qu0agGnkG-1E7bIcwnuW3OzBeRwrYrB3jKd_pGrb8"
        )
        == False
    )


def test_add_user_should_add_a_user(mocker):
    mocker.patch("src.controllers.auth.UserManager.does_user_exist", return_value=False)
    save_mock = mocker.patch("src.controllers.auth.UserManager.save")

    AuthenticationController.add_user("fake_user", "fake_password")

    assert save_mock.call_args[0][0].username == "fake_user"
    assert save_mock.call_args[0][0].password != "fake_password"


def test_add_user_should_throw_validation_error_if_user_exist(mocker):
    mocker.patch("src.controllers.auth.UserManager.does_user_exist", return_value=True)

    with pytest.raises(RuntimeError):
        AuthenticationController.add_user("fake_user", "fake_password")
