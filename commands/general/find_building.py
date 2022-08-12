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

from discord import Interaction
from discord.app_commands import Command

from controllers.find_building import get_building_information, is_valid_room_number


def command():
    return Command(
        name="salon",
        description=(
            "Provee información sobre el edificio donde se puede encontrar ese salón"
        ),
        callback=_find_building,
    )


async def _find_building(interaction: Interaction, salon: str):
    user_name = interaction.user.display_name

    if len(salon):
        if not is_valid_room_number(salon):
            await interaction.response.send_message(
                "No entendí el código de ese salon.\nIntenta escribirlo con guión."
            )
            return

        information = get_building_information(salon)

        if information:
            response_msg = (
                f"Hola {user_name}! Es posible que este salon se encuentre en el"
                f" edificio: **'{information['name']}'**\n{information['gmaps_loc']}"
            )

            await interaction.response.send_message(response_msg)
        else:
            response_msg = f"{user_name}, no sé en que edificio está salón. :("
            await interaction.response.send_message(response_msg)
    else:
        response_msg = (
            "No me especificaste cual salon quieres buscar.\nIntenta en este formato:"
            " !salon:*<código>*\nSi el salon contiene letras (ej: Fisica B) escribelo"
            " con guión. -> *!salon:F-B*"
        )
        await interaction.response.send_message(response_msg)
