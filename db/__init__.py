import pymongo
from pymongo.database import Database
import config
import log

__all__ = ["get_database", "close_db"]

__database: Database = None


def _init_db(mongo_client: pymongo.MongoClient = None):
    log.debug("Initing database...")

    global __database

    if mongo_client is None:
        mongo_client = pymongo.MongoClient(config.MONGO_CONNECTION_STRING)

    __database = mongo_client.get_database(config.MONGO_DB)

    if len(__database.list_collection_names()) == 0:
        __database.create_collection("empty")


def get_database():
    global __database

    if __database is None:
        _init_db()

    return __database


def close_db():
    __database.client.close()
