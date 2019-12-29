import pymongo
from flask import current_app

from typing import Optional


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return vars(self) == vars(other)


def get_mongo_client() -> pymongo.MongoClient:
    mongo_url = current_app.config["MONGO_URL"]
    mongo_port = current_app.config["MONGO_PORT"]
    return pymongo.MongoClient(mongo_url, mongo_port)


class UserManager:
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        pass

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
        pass
