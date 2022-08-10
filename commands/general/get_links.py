"""
//  /event_handlers/links.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 08/03/2021
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
import json
import os
import re
from datetime import datetime

import discord
from constants import paths
from discord.app_commands import Command


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
