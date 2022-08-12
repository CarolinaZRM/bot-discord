import logging
import unittest

import mongomock

import config
from db import close_db, get_database
from scripts.upload_prepas_csv import build_args, insert_into_db


class TestUploadPrepas(unittest.TestCase):
    def test_contains_all(self):
        arguments = build_args("-f test.csv".split())
        self.assertIn("file", arguments)
        self.assertIn("out", arguments)
        self.assertIn("collection", arguments)
        self.assertIn("production", arguments)

    def test_build_args_debug(self):
        arguments = build_args("-f test.csv".split())
        self.assertEqual(getattr(arguments, "collection"), "prepas")
        self.assertEqual(getattr(arguments, "production"), False)
        self.assertEqual(getattr(arguments, "out"), None)

    def test_build_args_production(self):
        arguments = build_args("-f test.csv --production".split())
        self.assertEqual(getattr(arguments, "collection"), "prepas")
        self.assertEqual(getattr(arguments, "production"), True)
        self.assertEqual(getattr(arguments, "out"), None)

    def test_build_args_change_collection(self):
        arguments_1 = build_args("-f test.csv --collection newname".split())
        self.assertEqual(getattr(arguments_1, "collection"), "newname")
        arguments_2 = build_args("-f test.csv -c newname".split())
        self.assertEqual(getattr(arguments_2, "collection"), "newname")

    @mongomock.patch(servers=config.MONGO_CONNECTION_STRING, on_new="create")
    def test_insert_into_db(self):
        prepas = [
            {
                "last_names": "RIVERA LOPEZ",
                "mother_lastname": "LOPEZ",
                "father_lastname": "RIVERA",
                "first_name": "JULIO",
                "middle_initial": "E",
                "email": "julio.rivera999@upr.edu",
                "program_id": "ICOM",
                "group_id": "Yoda",
            },
            {
                "last_names": "DEL PUEBO",
                "mother_lastname": "",
                "father_lastname": "DEL PUEBLO",
                "first_name": "JUAN",
                "middle_initial": "",
                "email": "juan.delpueblo@upr.edu",
                "program_id": "INEL",
                "group_id": "Mando",
            },
            {
                "last_names": "PEREZ BERRIOS",
                "mother_lastname": "BERRIOS",
                "father_lastname": "PEREZ",
                "first_name": "JOSHUA",
                "middle_initial": "A",
                "email": "joshua.perez5555@upr.edu",
                "program_id": "ICOM",
                "group_id": "BB8",
            },
        ]

        db_instance = get_database()
        prepa_collection = db_instance.get_collection("prepas")
        prepa_collection.drop()

        insert_into_db(prepa_collection.name, prepas)

        for i in prepa_collection.find():
            self.assertIn(i, prepas)

    def tearDown(self) -> None:
        close_db()
        return super().tearDown()
