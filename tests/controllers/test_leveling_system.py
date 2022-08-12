from ctypes import Union
import logging
import math
import sys
from typing import Any, Dict
import unittest
import mongomock
import config


from db import close_db, get_database

from controllers.leveling_system import general_leaderboard, add_experience, level_join


class TestLevelingSystem(unittest.TestCase):
    @classmethod
    @mongomock.patch(servers=config.MONGO_CONNECTION_STRING)
    def setUpClass(cls) -> None:
        cls.collection = get_database().get_collection("leaderboard")
        return super().setUpClass()

    def setUp(self) -> None:
        self.collection.insert_many(
            [
                {
                    "user_id": "718625533273047080",
                    "display_name": "Andrea Rodriguez Astacio",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                },
                {
                    "user_id": "263335918474231809",
                    "display_name": "Ivan Jackson",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                },
                {
                    "user_id": "700040383173754929",
                    "display_name": "Fernando Agosto Qui\u00f1ones",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                },
                {
                    "user_id": "871228485878833212",
                    "display_name": "Rial A Garcia Maldonado",
                    "experience": 5,
                    "level": 1,
                    "messages": 5,
                    "timestamp": 1660175447,
                },
                {
                    "user_id": "740304451285418085",
                    "display_name": "Valentina Ramirez Ramirez",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                },
                {
                    "user_id": "754442533454610533",
                    "display_name": "Jan K Rivera Reina",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                },
                {
                    "user_id": "740360832353042494",
                    "display_name": "Glorian Serrano",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                },
                {
                    "user_id": "475435563537793026",
                    "display_name": "CarolinaRM",
                    "experience": 223,
                    "level": 2,
                    "messages": 71,
                    "timestamp": 1659391479,
                },
                {
                    "user_id": "871530335693852742",
                    "display_name": "Jose R Rivera Rodriguez",
                    "experience": 0,
                    "level": 1,
                    "messages": 0,
                    "timestamp": 1628448840,
                },
                {
                    "user_id": "539112744553676812",
                    "display_name": "leirhab",
                    "experience": 10,
                    "level": 1,
                    "messages": 5,
                    "timestamp": 1660175454,
                },
                {
                    "user_id": "1003777102157455522",
                    "display_name": "Cesar Ruiz",
                    "experience": 20,
                    "level": 1,
                    "messages": 4,
                    "timestamp": 1659392734,
                },
                {
                    "user_id": "1003502626291322991",
                    "display_name": "Eduardo Novoa",
                    "experience": 5,
                    "level": 1,
                    "messages": 1,
                    "timestamp": 1659391568,
                },
                {
                    "user_id": "1003785352269549608",
                    "display_name": "Haziel",
                    "experience": 0,
                    "level": 1,
                    "messages": 1,
                    "timestamp": 1659391901,
                },
                {
                    "user_id": "1003786416662270012",
                    "display_name": "Luis A. Mu\u00f1oz",
                    "experience": 5,
                    "level": 1,
                    "messages": 2,
                    "timestamp": 1659393265,
                },
                {
                    "user_id": "458753143702945792",
                    "display_name": "--__--",
                    "experience": 5,
                    "level": 1,
                    "messages": 1,
                    "timestamp": 1659392149,
                },
                {
                    "user_id": "1003776105590829097",
                    "display_name": "Alex Vazquez",
                    "experience": 20,
                    "level": 1,
                    "messages": 10,
                    "timestamp": 1659394796,
                },
                {
                    "user_id": "712519464427454464",
                    "display_name": "END5E9",
                    "experience": 0,
                    "level": 1,
                    "messages": 1,
                    "timestamp": 1659392357,
                },
                {
                    "user_id": "839958747697774662",
                    "display_name": "Alpha-17",
                    "experience": 0,
                    "level": 1,
                    "messages": 1,
                    "timestamp": 1659392632,
                },
                {
                    "user_id": "977590463777349682",
                    "display_name": "Juan_D",
                    "experience": 5,
                    "level": 1,
                    "messages": 2,
                    "timestamp": 1659392900,
                },
            ]
        )
        return super().setUp()

    def test_get_leaderboard(self):
        expected = (
            {
                "user_id": "475435563537793026",
                "display_name": "CarolinaRM",
                "experience": 223,
                "level": 2,
                "messages": 71,
                "timestamp": 1659391479,
            },
            {
                "user_id": "1003777102157455522",
                "display_name": "Cesar Ruiz",
                "experience": 20,
                "level": 1,
                "messages": 4,
                "timestamp": 1659392734,
            },
            {
                "user_id": "1003776105590829097",
                "display_name": "Alex Vazquez",
                "experience": 20,
                "level": 1,
                "messages": 10,
                "timestamp": 1659394796,
            },
            {
                "user_id": "539112744553676812",
                "display_name": "leirhab",
                "experience": 10,
                "level": 1,
                "messages": 5,
                "timestamp": 1660175454,
            },
            {
                "user_id": "871228485878833212",
                "display_name": "Rial A Garcia Maldonado",
                "experience": 5,
                "level": 1,
                "messages": 5,
                "timestamp": 1660175447,
            },
            {
                "user_id": "1003502626291322991",
                "display_name": "Eduardo Novoa",
                "experience": 5,
                "level": 1,
                "messages": 1,
                "timestamp": 1659391568,
            },
            {
                "user_id": "1003786416662270012",
                "display_name": "Luis A. Muñoz",
                "experience": 5,
                "level": 1,
                "messages": 2,
                "timestamp": 1659393265,
            },
            {
                "user_id": "458753143702945792",
                "display_name": "--__--",
                "experience": 5,
                "level": 1,
                "messages": 1,
                "timestamp": 1659392149,
            },
            {
                "user_id": "977590463777349682",
                "display_name": "Juan_D",
                "experience": 5,
                "level": 1,
                "messages": 2,
                "timestamp": 1659392900,
            },
            {
                "user_id": "718625533273047080",
                "display_name": "Andrea Rodriguez Astacio",
                "experience": 0,
                "level": 1,
                "messages": 0,
            },
        )

        ids = tuple(map(lambda user: user.get("user_id"), expected))

        members_list = general_leaderboard()
        cnt = 0
        prev: int = sys.maxsize
        for member in members_list:
            member: Dict[str, Union[str, int]]
            self.assertGreaterEqual(prev, member.get("experience"))
            prev = member.get("experience")
            cnt += 1
            self.assertIn(
                member.get("user_id"), ids, f"Member {member} not in Expected."
            )

        self.assertEqual(cnt, 10)

    def test_add_experience_existing_user(self):
        original_user = self.collection.find_one({"user_id": "977590463777349682"})
        exp_change_res = add_experience(
            "977590463777349682", original_user["display_name"], 4
        )
        self.assertEqual(exp_change_res.modified_count, 1)

        modified_user: Dict[str, Any] = self.collection.find_one(
            {"user_id": "977590463777349682"}
        )
        self.assertEqual(modified_user.get("experience"), 9)
        self.assertEqual(modified_user.get("level"), 1)

    def test_add_experience_existing_user_integer_id(self):
        original_user = self.collection.find_one({"user_id": "977590463777349682"})

        exp_change_res = add_experience(
            int("977590463777349682"), original_user["display_name"], 4
        )

        self.assertEqual(exp_change_res.modified_count, 1)

        modified_user: Dict[str, Any] = self.collection.find_one(
            {"user_id": "977590463777349682"}
        )
        self.assertEqual(modified_user.get("experience"), 9)
        self.assertEqual(modified_user.get("level"), 1)

    def test_add_experience_not_existing_user(self):
        exp_change_res = add_experience("NOT_EXISTS", "John Doe", 4)
        self.assertEqual(exp_change_res.modified_count, 1)

        new_user: Dict[str, Any] = self.collection.find_one({"user_id": "NOT_EXISTS"})

        self.assertIsNotNone(new_user.get("display_name"), "John Doe")
        self.assertIsNotNone(new_user.get("experience"), 4)
        self.assertIsNotNone(new_user.get("level"), 1)
        self.assertIsNotNone(new_user.get("messages"), 1)
        self.assertIsNotNone(new_user.get("user_id"), "NOT_EXISTS")

    def test_level_on_join(self):
        user_id = "NOT_EXISTS"

        self.assertIsNone(self.collection.find_one({"user_id": user_id}))

        level_join(user_id, "Juan Del Pueblo")

        user_info: Dict[str, Any] = self.collection.find_one({"user_id": user_id})
        logging.debug(user_info)
        self.assertIsNotNone(user_info)

        user_info.pop("_id", None)
        self.assertEqual(
            user_info,
            {
                "user_id": "NOT_EXISTS",
                "display_name": "Juan Del Pueblo",
                "messages": 0,
                "level": 1,
            },
        )

    def tearDown(self) -> None:
        self.collection.drop()
        return super().tearDown()
