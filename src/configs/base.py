import os

SECRET_KEY = os.getenv("FLASK_KEY")
JWT_KEY = os.getenv("JWT_KEY")

MONGO_PORT = 27017
