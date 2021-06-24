"""
//  get_building_information.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021.
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

import re

from .buildings import buildings_list


def get_building_information(sections):
    if len(sections) == 1:
        return False

    salon = sections[1]

    salon_splited = re.split('-', salon)

    regex_result = re.findall("^\D+", salon_splited[0])

    if len(regex_result) != 1:
        return False

    text_part_of_code: str = regex_result[0].lower()

    if text_part_of_code in buildings_list:
        return buildings_list[text_part_of_code]
    else:
        return False
