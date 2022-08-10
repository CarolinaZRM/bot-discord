'''
//  /event_handlers/links.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 08/03/2021
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
from datetime import datetime
import discord
import re
import json
from constants import paths
import os

print(paths.EMBEDS, 'links.json')


_EMBED_PATH = os.path.join(paths.EMBEDS, 'links.json')


_EMBED: discord.Embed = None

with open(_EMBED_PATH, 'r') as embed_file:
    _EMBED = discord.Embed.from_dict(json.load(embed_file))

_EMBED.colour = discord.Colour.dark_magenta()


async def event_links(message: discord.Message):
    CMD = '!links'

    if not re.fullmatch(CMD, message.content):
        return

    _EMBED.timestamp = datetime.now()

    await message.channel.send(embed=_EMBED)
