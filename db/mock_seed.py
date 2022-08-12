import mongomock
import json

from constants import paths


def load_mock_data(database: mongomock.Database):
    with open(paths.ROOT_PATH + "/db/data/leaderboard.json", "r") as data_file:
        leaderboard_data = json.load(data_file)
        database.get_collection("leaderboard").insert_many(leaderboard_data)
