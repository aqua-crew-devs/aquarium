from werkzeug.security import check_password_hash

from src.models.user import UserManager


class AuthenticationController:
    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        user = UserManager.get_by_username(username)
        if user is None:
            return False
        return check_password_hash(user.password, password)

    @staticmethod
    def issue_token(username: str) -> str:
        pass

    @staticmethod
    def verify_token(token: str) -> bool:
        pass

