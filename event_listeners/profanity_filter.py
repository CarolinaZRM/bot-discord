"""
//  /bot-discord/event_listeners/profanity_filter.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/14
//
//  Last Modified: Sunday, 14th August 2022 1:51:43 am
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import os

# https://github.com/snguyenthanh/better_profanity
from better_profanity import profanity
from discord import Message

import log
from bot import is_from_a_channel
from constants import paths

_PROFANITY_FILE_PATH = os.path.join(paths.TEXT_FILES, "profanities.txt")


def __init_sanitize():
    log.info("[VERBOSE] Initializing additional Spanish Profanities")
    censored_spanish_words = open(_PROFANITY_FILE_PATH, "r")

    lines = censored_spanish_words.readlines()
    censored_spanish_words.close()
    lines = list(map(lambda x: x.strip().lower(), lines))

    combinations = set()
    for word in lines:
        num_of_non_allowed_chars = profanity._count_non_allowed_characters(word)
        if num_of_non_allowed_chars > profanity.MAX_NUMBER_COMBINATIONS:
            profanity.MAX_NUMBER_COMBINATIONS = num_of_non_allowed_chars

        combinations.update(set(profanity._generate_patterns_from_word(word)))

    profanity.add_censor_words(combinations)
    log.info("[VERBOSE] Finished adding additional Spanish Profanities")


__init_sanitize()


async def on_message(message: Message) -> bool:
    """
    If message contains a profanity return `True`, else return `False`
    """
    if not is_from_a_channel(message):
        return False

    user_message = message.content
    if profanity.contains_profanity(user_message):
        author = message.author.display_name
        channel_sent = message.channel
        log.info(f"{author} dijo una profanidad, borré el mensaje. {user_message}")
        await message.delete(delay=0)
        await channel_sent.send(f"{author} dijo una profanidad, borré el mensaje")
        return True
    return False
