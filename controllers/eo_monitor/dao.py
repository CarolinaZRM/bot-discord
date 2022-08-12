"""
//  /bot-discord/controllers/admin_monitor/dao.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 4:24:18 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from typing import Dict, List, Union

from db import Cursor, get_database


def get_student_orientator(username: str) -> Union[Dict[str, str], None]:
    counselor_collection = get_database().get_collection("student_orientators")
    return counselor_collection.find_one({"username": username})


def add_user_to_eo(username: str) -> None:
    counselor_collection = get_database().get_collection("student_orientators")
    counselor_collection.insert_one({"username": username})


def update_eo_list(eo_username_list: List[str]) -> int:
    if len(eo_username_list) == 0:
        return 0

    counselor_collection = get_database().get_collection("student_orientators")

    existing_eo_cursor: Cursor = counselor_collection.find(
        {"username": {"$in": eo_username_list}}
    )

    new_eos = set(eo_username_list).difference(
        map(lambda x: x["username"], existing_eo_cursor)
    )

    if len(new_eos) == 0:
        return 0

    return len(
        counselor_collection.insert_many(
            [{"username": user_} for user_ in new_eos]
        ).inserted_ids
    )
