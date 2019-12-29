from typing import Optional


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return vars(self) == vars(other)


class UserManager:
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        pass
