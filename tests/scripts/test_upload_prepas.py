from ast import arguments
import unittest

import config
import mongomock

import logging

from db import get_database, close_db

from scripts.upload_prepas_csv import build_args, main


class TestUploadPrepas(unittest.TestCase):
    @mongomock.patch(servers=config.MONGO_CONNECTION_STRING)
    def test_is_uploading(self):
        db_instance = get_database()
        logging.debug(db_instance)

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
