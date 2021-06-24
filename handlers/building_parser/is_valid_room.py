"""
//  is_valid_room.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021.
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

import re


def is_valid_room_number(sections):
    if len(sections) == 1:
        return False

    tmp = sections[1]

    regex_result = re.findall("^\D+", tmp)

    if len(regex_result) == 1:
        return True

    return False
