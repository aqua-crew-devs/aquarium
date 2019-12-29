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
