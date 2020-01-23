from flask import current_app
import pymongo


def get_mongo_client() -> pymongo.MongoClient:
    mongo_url = current_app.config["MONGO_URL"]
    mongo_port = current_app.config["MONGO_PORT"]
    return pymongo.MongoClient(mongo_url, mongo_port)
