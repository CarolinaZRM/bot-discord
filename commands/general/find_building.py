"""
//  /bot-discord/commands/general/find_building.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/10
//
//  Last Modified: Wednesday, 10th August 2022 6:20:11 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

import re

from discord import Interaction
from discord.app_commands import Command

import log
from controllers.find_building import get_building_information


def command():
    return Command(
        name="salon",
        description=(
            "Provee información sobre el edificio donde se puede encontrar ese salón"
        ),
        callback=_find_building,
    )


def _format_classroom(salon: str):
    internal_ = salon.replace("-", "")
    letters = re.findall("^\D+", internal_)
    numbers = re.findall("\d+$", internal_)
    if numbers and letters:
        return str(letters[0]).upper() + "-" + numbers[0]

    if letters:
        return str(letters[0]).upper()

    return salon


async def _find_building(interaction: Interaction, salon: str):
    user_name = interaction.user.display_name
    log.debug("enrty: " + salon + str(len(salon)))
    formatted_salon = _format_classroom(salon)
    if len(salon):
        information = get_building_information(salon)
        if information:
            response_msg = (
                f'Hola {user_name}! Es posible que el salón "{formatted_salon}" se'
                " encuentre en el edificio:"
                f" **'{information['name']}'**\n{information['gmaps_loc']}"
            )
            await interaction.response.send_message(response_msg)
        else:
            response_msg = (
                f"{user_name}, no sé en que edificio está el salón"
                f' "{formatted_salon}". :('
            )
            log.debug(response_msg)
            await interaction.response.send_message(response_msg)
    else:
        response_msg = (
            "No me especificaste cual salon quieres buscar.\nIntenta en este formato:"
            " !salon:*<código>*\nSi el salon contiene letras (ej: Fisica B) escribelo"
            " con guión. -> *!salon:F-B*"
        )
        log.debug(response_msg)
        await interaction.response.send_message(response_msg)
