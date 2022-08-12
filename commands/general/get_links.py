"""
//  /home/gbrl18/bot-discord/commands/general/get_links.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 10:39:57 am
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

import json
import os
from datetime import datetime

import discord
from discord.app_commands import Command

from constants import paths

_EMBED: discord.Embed = None


def command():
    return Command(
        name="links",
        description="Una lista curada de enlaces importantes",
        callback=_get_links,
    )


def __init() -> None:
    global _EMBED
    _EMBED_PATH = os.path.join(paths.EMBEDS, "links.json")

    with open(_EMBED_PATH, "r") as embed_file:
        _EMBED = discord.Embed.from_dict(json.load(embed_file))

    _EMBED.colour = discord.Colour.dark_magenta()


async def _get_links(interaction: discord.Interaction):
    global _EMBED
    if _EMBED is None:
        __init()

    _EMBED.timestamp = datetime.now()

    await interaction.response.send_message(embed=_EMBED)
