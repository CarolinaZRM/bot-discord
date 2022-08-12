"""
//  /bot-discord/tests/db/test_db_connection.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/11
//  
//  Last Modified: Thursday, 11th August 2022 1:34:14 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import logging
import unittest

import config
import mongomock

from db import close_db, get_database


class MongoDbTest(unittest.TestCase):
    @mongomock.patch(servers=(config.MONGO_CONNECTION_STRING))
    def test_inserts(self):
        objects = [dict(votes=1), dict(votes=2)]

        database_instance = get_database()
        logging.debug(database_instance)

        database_instance.get_collection("prepas").insert_many(objects)

        results = get_database().get_collection("prepas").find()

        for obj_ in objects:
            self.assertIn(obj_, results)

    @mongomock.patch(servers=(config.MONGO_CONNECTION_STRING))
    def tearDown(self) -> None:
        close_db()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
