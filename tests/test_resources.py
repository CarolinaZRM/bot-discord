"""
//  /bot-discord/tests/test_resources.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 9:38:18 am
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import datetime
import sys
import unittest


class ExpiredResourceException(Exception):
    pass


def get_curr_func():
    return f"{sys._getframe(1).f_code.co_name}_verified"


class ResourceTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.today = datetime.datetime.now()

        if self.today.month < 8:
            self.due_date = datetime.datetime(self.today.year, 6, 1, 0, 0, 0)
        else:
            self.due_date = datetime.datetime(self.today.year + 1, 6, 1, 0, 0, 0)

    RESOURCE_MAP = {
        "Curriculos_verified": False,
        "Embeds_verified": False,
        "Images_verified": False,
        "Prepas_verified": False,
        "Proyectos_verified": False,
        "Faq_verified": False,
        "Counselors_verified": False,
        "Rules_verified": False,
        "Guia_prepistica_verified": False,
        "Organizations_info_verified": False,
    }

    def test_expirations(self):
        for to_verify, is_verified in self.RESOURCE_MAP.items():
            if (self.today.month > 7 or self.today.month < 6) and is_verified is True:
                raise Exception("Out of verification period. Reset FLAGS to False")

            if not is_verified and datetime.datetime.now() > self.due_date:
                raise ExpiredResourceException(
                    f"\"{to_verify.split('_')[0]}\" are expired verify and change the"
                    " VERIFIED Flag."
                )


if __name__ == "__main__":
    unittest.main(verbosity=1)
