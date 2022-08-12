"""
//  /bot-discord/tests/controllers/test_admin_monitor.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 5:07:52 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import unittest

import mongomock

import config
from controllers.eo_monitor.dao import (
    add_user_to_eo,
    get_student_orientator,
    update_eo_list,
)
from db import get_database


class TestLevelingSystem(unittest.TestCase):
    @classmethod
    @mongomock.patch(servers=config.MONGO_CONNECTION_STRING)
    def setUpClass(cls) -> None:
        cls.collection = get_database().get_collection("student_orientators")
        return super().setUpClass()

    def setUp(self) -> None:
        self.collection.insert_many(
            [{"username": "aristoteles.ts#4359"}, {"username": "leirhab#4359"}]
        )
        return super().setUp()

    def test_get_eo(self):
        eo_obj = get_student_orientator("leirhab#4359")
        self.assertIsNotNone(eo_obj)
        eo_obj.pop("_id", None)
        self.assertEqual(eo_obj, {"username": "leirhab#4359"})

    def test_add_eo(self):
        add_user_to_eo("new#4359")
        new_eo = self.collection.find_one({"username": "new#4359"})
        self.assertIsNotNone(new_eo)
        self.assertEqual(new_eo["username"], "new#4359")

    def test_add_eo_with_existing(self):
        eos = [
            "newnew",
            "aristoteles.ts#4359",
            "leirhab#4359",
        ]

        new_ids_count = update_eo_list(eos)

        self.assertEqual(new_ids_count, 1)

        new_obj = self.collection.find({"username": "newnew"})
        self.assertIsNotNone(new_obj, None)

    def test_add_eo_only_existing(self):
        eos = [
            "aristoteles.ts#4359",
            "leirhab#4359",
        ]
        new_ids_count = update_eo_list(eos)
        self.assertEqual(new_ids_count, 0)

    def test_add_eo_only_non_existing(self):
        eos = [
            "newnewnew_1",
            "newnewnew_2",
        ]
        new_ids_count = update_eo_list(eos)
        self.assertEqual(new_ids_count, 2)

    def tearDown(self) -> None:
        self.collection.drop()
        return super().tearDown()
