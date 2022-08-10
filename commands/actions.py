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
_MADE_WEBSITE = os.path.join(paths.IMAGES, "MadeWeb.png")

# PDF Files
CURRICULO_INEL = os.path.join(paths.CURRICULOS, "INEL.pdf")
CURRICULO_INSO = os.path.join(paths.CURRICULOS, "INSO.pdf")
CURRICULO_CIIC = os.path.join(paths.CURRICULOS, "CIIC.pdf")
CURRICULO_ICOM = os.path.join(paths.CURRICULOS, "ICOM.pdf")


async def event_get_curriculum(message: discord.Message):
    log.info("Entered Curriculum")
    user_message = message.content
    if "!curriculo" in user_message.lower():  # Asked for curriculum
        split = user_message.split(":")
        log.info("Contains Curriculum")
        if len(split) == 1:
            await message.author.send(
                "No me dijiste que curriculo necesitas :slight_frown:\nIntenta con: INEL/ICOM/INSO/CIIC"
            )
        else:
            if split[1].upper() == "INEL":
                await message.author.send(
                    "Here is the Electrical Engineering Curriculum:"
                )
                await message.author.send(file=discord.File(CURRICULO_INEL))
            if split[1].upper() == "ICOM":
                await message.author.send(
                    "Here is the Computer Engineering Curriculum:"
                )
                await message.author.send(file=discord.File(CURRICULO_ICOM))
            if split[1].upper() == "INSO":
                await message.author.send(
                    "Here is the Software Engineering Curriculum:"
                )
                await message.author.send(file=discord.File(CURRICULO_INSO))
            if split[1].upper() == "CIIC":
                await message.author.send(
                    "Here is the Computer Science & Engineering Curriculum:"
                )
                # for when CIIC curriculum is updated
                await message.author.send(file=discord.File(CURRICULO_CIIC))


# EMBED EX


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


async def get_made_website(message: discord.Message):
    log.debug("[DEBUG] ENTERED MADE'S WEBSITE COMMAND")
    usr_msg = message.content
    if usr_msg.lower() == "!madeweb":
        await message.author.send(
            "Aquí el enlace para la página web de Made! :green_heart: \n "
            "https://sites.google.com/upr.edu/maderodriguez/",
            file=discord.File(_MADE_WEBSITE),
        )
        # await message.author.send(file=)
