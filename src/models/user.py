from .database import get_mongo_client

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
        users = get_mongo_client().aquarium.users

        user = users.find_one({"username": username})
        if user is None:
            return None
        return User(username=user["username"], password=user["password"])

    @staticmethod
    def save(user: User):
        users = get_mongo_client().aquarium.users

        users.find_one_and_replace(
            {"username": user.username},
            {"username": user.username, "password": user.password},
            upsert=True,
        )

    @staticmethod
    def does_user_exist(username: str) -> bool:
        return UserManager.get_by_username(username) is not None

