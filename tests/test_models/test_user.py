import pymongo
import mongomock

from src.models.user import User, UserManager

TEST_MONGO_SERVERS = (("localhost", 27017),)


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_add_a_user_if_there_is_no_such_user(app):
    with app.app_context():
        UserManager.save(User("fake_user", "fake_password"))

        users = pymongo.MongoClient("localhost", 27017).aquarium.users
        user = users.find_one({"username": "fake_user"})
        assert user is not None
        assert user["password"] == "fake_password"


@mongomock.patch(servers=TEST_MONGO_SERVERS)
def test_it_should_update_user_if_there_is_such_a_user(app):
    with app.app_context():
        users = pymongo.MongoClient("localhost", 27017).aquarium.users
        users.insert_one({"username": "fake_user", "password": "old_password"})

        UserManager.save(User("fake_user", "new_password"))
        user = users.find_one({"username": "fake_user"})
        assert user is not None
        assert user["password"] == "new_password"
