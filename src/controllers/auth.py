from datetime import datetime, timedelta

import jwt
from werkzeug.security import check_password_hash

from src.models.user import UserManager


def get_jwt_secret() -> str:
    pass


class AuthenticationController:
    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        user = UserManager.get_by_username(username)
        if user is None:
            return False
        return check_password_hash(user.password, password)

    @staticmethod
    def issue_token(username: str, expired_in_sec: int) -> str:
        expired_at = datetime.utcnow() + timedelta(seconds=expired_in_sec)
        return jwt.encode(
            {
                "username": username,
                "expired_at": expired_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
            get_jwt_secret(),
            algorithm="HS256",
        )

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            decoded_token = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])

            return datetime.utcnow() < datetime.strptime(
                decoded_token["expired_at"], "%Y-%m-%d %H:%M:%S"
            )
        except:
            return False

