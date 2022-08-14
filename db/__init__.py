import mongomock
import pymongo
from pymongo.cursor import Cursor

import config
import log
from db import mock_seed

__all__ = ["get_database", "close_db", "Cursor"]

__mongo_client: pymongo.MongoClient = None


def get_database():
    global __mongo_client

    if __mongo_client is None:
        _init_client()

    return __mongo_client.get_database(config.MONGO_DB)


def close_db():
    if __mongo_client:
        __mongo_client.close()


def _init_client(mongo_client: pymongo.MongoClient = None):
    global __mongo_client
    log.debug("Initializing MongoDb Client...")

    if (config.MONGO_MOCK or "").lower() == "true":
        mongo_client = mongomock.MongoClient(
            config.MONGO_CONNECTION_STRING
        )  # fake Server
        mock_seed.load_mock_data(mongo_client.get_database(config.MONGO_DB))
    else:
        mongo_client = pymongo.MongoClient(config.MONGO_CONNECTION_STRING)
        database = mongo_client.get_database(config.MONGO_DB)
        if len(database.list_collection_names()) == 0:
            database.create_collection("empty")

    __mongo_client = mongo_client
