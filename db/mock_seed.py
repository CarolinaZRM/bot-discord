import json
from pathlib import Path

import mongomock

from constants import paths


def load_mock_data(database: mongomock.Database):
    DATA_PATH = Path(paths.ROOT_PATH + "/db/mock-data")

    with open(DATA_PATH / "leaderboard.json", "r") as lb_data_file:
        leaderboard_data = json.load(lb_data_file)
        database.get_collection("leaderboard").insert_many(leaderboard_data)

    with open(DATA_PATH / "prepas.json", "r") as prepa_data_file:
        prepas_data = json.load(prepa_data_file)
        database.get_collection("prepas").insert_many(prepas_data)
