import pymongo
from pymongo.database import Database
import config

__all__ = ["database", "close_db"]


def __init_db():
    mongo_client = pymongo.MongoClient(config.MONGO_CONNECTION_STRING)

    if config.MONGO_DB not in mongo_client.list_database_names():
        raise Exception(
            f"BotException: {config.MONGO_DB} database does not exist in Mongo Server"
        )

    return mongo_client.get_database(config.MONGO_DB)


database: Database = __init_db()


def close_db():
    database.client.close()
