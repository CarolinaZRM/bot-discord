"""
//
//  actions.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""

import json
import os
import os.path
from typing import Dict

import discord
import log
from constants import paths

# files
_PROJECT_FILE = os.path.join(paths.PROJECTS, "proyectos.json")


async def get_prj_info(message: discord.Message):
    log.info("Entered Project")

    user_message = message.content

    if "!ls_projects" not in user_message.lower():
        return

    split = user_message.split(":")

    with open(_PROJECT_FILE, "r") as fi:
        proyectos: Dict = json.load(fi)

        mess = ", ".join(proyectos.keys())

        if len(split) == 1:
            await message.author.send(
                "No me dijiste el nombre del proyecto que quieres buscar.\nIntenta con: "
                + mess
            )
            return

        key = split[1]
        if proyectos.get(key) is None:
            await message.author.send(
                "No tenemos información de este proyecto.\nIntenta con: " + mess
            )
            return

        embed: discord.Embed = discord.Embed.from_dict(proyectos[key])
        await message.author.send(
            content=f"Esta es la información del {key}\n", embed=embed
        )
