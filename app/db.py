from flask import current_app, g
from pymongo import MongoClient


def get_client():
    if "mongo_client" not in g:
        factory = current_app.config.get("MONGO_CLIENT_FACTORY", MongoClient)
        g.mongo_client = factory(
            current_app.config["MONGO_URI"],
            serverSelectionTimeoutMS=current_app.config["MONGO_TIMEOUT_MS"],
        )
    return g.mongo_client


def get_db():
    return get_client()[current_app.config["MONGO_DB_NAME"]]


def close_db(_error=None):
    client = g.pop("mongo_client", None)
    if client is not None:
        client.close()
