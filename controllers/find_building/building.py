"""
//  get_building_information.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021.
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

import re
from typing import Dict, Union

from .building_list import buildings_list


def get_building_information(salon: str) -> Union[Dict[str, str], None]:
    salon_splited = re.split("-", salon)  # case 1, s-123, ch-123

    regex_result = re.findall("^\D+", salon_splited[0])

    if len(regex_result) != 1:
        return False

    text_part_of_code: str = regex_result[0].lower()
    building_info = buildings_list.get(text_part_of_code, None)

    return building_info
