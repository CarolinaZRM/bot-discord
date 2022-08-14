"""
//  /bot-discord/commands/server_management/add_word_to_censor.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/14
//
//  Last Modified: Sunday, 14th August 2022 1:06:25 am
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import os

# https://github.com/snguyenthanh/better_profanity
from better_profanity import profanity
from discord import Interaction
from discord.app_commands import Command

import log
from bot import is_sender_admin
from constants import paths

_PROFANITY_FILE_PATH = os.path.join(paths.TEXT_FILES, "profanities.txt")


def command():
    return Command(
        name="add-profanity",
        description="Add word to censor list",
        callback=_add_profanity_to_list,
    )


async def _add_profanity_to_list(interaction: Interaction, profanity_to_add: str):
    if profanity_to_add is None:
        return await interaction.response.send_message(
            "No me dijiste que palabra añado a la lista de profanidades",
            ephemeral=True,
        )

    if is_sender_admin(interaction.user):
        log.info("Can add a profanity. Is ADMIN")

        censored_words_file = open(_PROFANITY_FILE_PATH, "r")
        lines = censored_words_file.readlines()
        censored_words_file.close()
        censored_words = set(map(lambda x: x.strip().lower(), lines))
        censored_words_file.close()

        profanity_to_add = profanity_to_add.lower()

        if profanity_to_add not in censored_words:
            profanity_file = open(_PROFANITY_FILE_PATH, "a+")
            profanity_file.writelines(f"{profanity_to_add}\n")
            profanity_file.close()

            combinations = set()
            combinations.update(profanity._generate_patterns_from_word(profanity_to_add))
            profanity.add_censor_words(combinations)

        await interaction.response.send_message(
            f"{interaction.user.display_name}, commando fue completado",
            ephemeral=True,
        )
    else:
        log.debug(f"User {interaction.user} is not counselor")
        await interaction.response.defer(thinking=False)
        await interaction.delete_original_message()
