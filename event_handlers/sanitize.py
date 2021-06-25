# https://github.com/snguyenthanh/better_profanity
"""
//
//  sanitize.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
from better_profanity import profanity
import discord
import log
import os
from bot import is_sender_counselor, is_from_a_channel

_CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
_PROFANITY_FILE_PATH = os.path.join(
    _CURRENT_DIR, "res", "textfiles", "profanities.txt")


def __init_sanitize():
    global _CURRENT_DIR
    log.debug('[VERBOSE] Initializing additional Spanish Profanities')
    censored_spanish_words = open(_PROFANITY_FILE_PATH, 'r')

    lines = censored_spanish_words.readlines()
    censored_spanish_words.close()
    lines = list(map(lambda x: x.strip().lower(), lines))

    combinations = set()
    for word in lines:
        num_of_non_allowed_chars = profanity._count_non_allowed_characters(
            word)
        if num_of_non_allowed_chars > profanity.MAX_NUMBER_COMBINATIONS:
            profanity.MAX_NUMBER_COMBINATIONS = num_of_non_allowed_chars

        combinations.update(
            set(profanity._generate_patterns_from_word(word)))

    profanity.add_censor_words(combinations)
    log.debug('[VERBOSE] Finished adding additional Spanish Profanities')


__init_sanitize()


async def add_profanity_to_list(message: discord.Message):
    sections = message.content.split(':')
    if sections[0] == "!admin_add_profanity":
        if len(sections) == 1:
            await message.author.send("No me dijiste que palabra añado a la lista de profanidades")
            return

        if is_sender_counselor(message):
            author = None
            if hasattr(message.author, 'nick'):
                author = message.author.nick
            else:
                author = message.author.name
            log.debug('[DEBUG] Can add a profanity. Is ADMIN')

            censored_words_file = open(_PROFANITY_FILE_PATH, 'r')
            lines = censored_words_file.readlines()
            censored_words_file.close()
            censored_words = set(list(map(lambda x: x.strip().lower(), lines)))
            censored_words_file.close()

            profanity_to_add = sections[1].lower()

            if profanity_to_add not in censored_words:
                profanity_file = open(_PROFANITY_FILE_PATH, 'a+')
                profanity_file.write(f'{profanity_to_add}\n')
                profanity_file.close()

                combinations = set()
                combinations.update(
                    profanity._generate_patterns_from_word(profanity_to_add)
                )
                profanity.add_censor_words(combinations)

            await message.delete(delay=0)
            await message.channel.send(f"""{author}, commando fue completado""")
            return True


async def profanity_filter(message: discord.Message) -> None:
    """
    If message contains a profanity return `True`, else return `False`
    """
    if not is_from_a_channel(message):
        return

    user_message = message.content
    if profanity.contains_profanity(user_message):
        # if better_profanity.profanity.contains_profanity(message.content):
        channel_sent = message.channel
        log.debug(f'Containes a bad word: {user_message}')
        author = None
        if hasattr(message.author, 'nick'):
            author = message.author.nick
        else:
            author = message.author.name
        await message.delete(delay=0)
        print(f"""{author} dijo una profanidad, borré el mensaje""")
        await channel_sent.send(f"""{author} dijo una profanidad, borré el mensaje""")
        return True
    return False
