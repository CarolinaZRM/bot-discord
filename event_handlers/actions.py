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
from controllers import building_parser

# files
_PROJECT_FILE = os.path.join(paths.PROJECTS, "proyectos.json")

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


async def event_parse_university_building(message: discord.Message):
    client_message: str = message.content
    sections = client_message.split(":")

    user_name = None

    if hasattr(message.author, "nick"):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    # response = f'Hola {user_name}, Es posible que este salon se encuentre en el edificio:\n'
    if len(sections) > 1 and sections[0] == "!salon" and len(sections[1]) > 0:

        if not building_parser.is_valid_room_number(sections):
            await message.channel.send(
                "No entendí el código de ese salon.\nIntenta escribirlo con guión."
            )
            return

        information = building_parser.get_building_information(sections)

        if information:
            response_msg = (
                f"Hola {user_name}! Es posible que este salon se encuentre en el edificio: **'{information['name']}'**\n"
                f"{information['gmaps_loc']}"
            )

            await message.channel.send(response_msg)
        else:
            response_msg = f"{user_name}, no sé en que edificio está salón. :("
            await message.channel.send(response_msg)
    elif sections[0] == "!salon":
        response_msg = (
            "No me especificaste cual salon quieres buscar.\nIntenta en este formato: !salon:*<código>*\n"
            "Si el salon contiene letras (ej: Fisica B) escribelo con guión. -> *!salon:F-B*"
        )
        await message.channel.send(response_msg)


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
