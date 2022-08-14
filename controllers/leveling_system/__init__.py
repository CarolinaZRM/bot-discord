"""
// /bot-discord/controllers/leveling_system/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/11
//
//  Last Modified: Thursday, 11th August 2022 4:08:08 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import time
from typing import Dict, Union

import discord
from pymongo import DESCENDING as PYMONGO_DESCENDING

import log
from db import get_database


class ExperienceChangeResult:
    def __init__(self, modified_count: int, new_level: int, old_level: int) -> None:
        self.modified_count = modified_count
        self.new_level = new_level
        self.old_level = old_level

    def leveled_up(self):
        return self.new_level > self.old_level


def calculate_level(start_level: int, total_experience: int):
    return max(1, int(total_experience / (100 + ((start_level - 1) * 15))))


def level_join(user_id: str, display_name: str):
    lb_collection = get_database().get_collection("leaderboard")

    if lb_collection.find_one({"user_id": str(user_id)}):
        # user already exists
        return

    lb_collection.insert_one(
        {
            "user_id": user_id,
            "display_name": display_name,
            "messages": 0,
            "level": 1,
        }
    )


# Add a variable number of exp to the json file for a user
def add_experience(
    user_id: str, display_name: str, exp_to_add: int
) -> Union[ExperienceChangeResult, None]:
    leaderboard_collection = get_database().get_collection("leaderboard")
    user_id = str(user_id)

    user_info = leaderboard_collection.find_one({"user_id": user_id})

    if not user_info:
        log.debug(f"User {user_id} does not exist: {user_info}")
        # user does not exists
        user_info = {
            "display_name": display_name,
            "experience": exp_to_add,
            "level": calculate_level(1, exp_to_add),
            "messages": 1,
            "timestamp": int(time.time()),
            "user_id": user_id,
        }
        leaderboard_collection.insert_one(user_info)
        return ExperienceChangeResult(1, 1, 1)

    log.debug(f"User {user_id} exists")

    BUFFER = 15  # seconds
    current_time = int(time.time())
    if "timestamp" in user_info:
        if current_time < BUFFER + user_info["timestamp"]:
            # return if buffer has not been completed
            return None

    old_level = user_info["level"]
    new_level = calculate_level(old_level, user_info["experience"])
    log.debug(f"Add exp for #{user_id} | {display_name} | Adding: #{exp_to_add}")

    result = leaderboard_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "display_name": display_name,
                "level": new_level,
                "timestamp": int(time.time()),
            },
            "$inc": {
                "experience": exp_to_add,
                "messages": 1,
            },
        },
    )

    return ExperienceChangeResult(result.modified_count, new_level, old_level)


def general_leaderboard():
    leaderboard_collection = get_database().get_collection("leaderboard")
    top_peeps = (
        leaderboard_collection.find().sort("experience", PYMONGO_DESCENDING).limit(10)
    )
    for item in top_peeps:
        yield item


def get_level_info(user_id: str) -> Union[Dict[str, str], None]:
    lb_collection = get_database().get_collection("leaderboard")
    return lb_collection.find_one({"user_id": str(user_id)})


# Runs on message, the user is given a certain amount of experience for each message
# and we check for level up
async def on_message(message: discord.Message) -> None:
    log.debug("Running leveling system listener...")
    user_id: str = str(message.author.id)
    display_name: str = message.author.display_name
    message_length: int = len(message.content)

    exp = min(message_length, 5)

    exp_change_result = add_experience(user_id, display_name, exp)

    if exp_change_result and exp_change_result.leveled_up():
        await message.channel.send(
            f"{message.author.mention} has leveled up to level"
            f" {exp_change_result.new_level}"
        )
