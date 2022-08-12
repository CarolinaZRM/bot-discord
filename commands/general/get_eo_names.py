"""
//  /bot-discord/commands/general/get_eo_names.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 3:32:31 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from typing import Set

import discord
from discord import Interaction, Member
from discord.app_commands import Command

import log
from commands.utils.autocomplete import program_autocomplete
from controllers import eo_monitor


def command():
    command = Command(
        name="estudiantes-orientadores",
        description="Get EOs de un programa",
        callback=_get_counselor_names,
    )

    command.autocomplete("program")(program_autocomplete)

    return command


async def _get_counselor_names(interaction: Interaction, program: str):
    log.info(f"Get counselor list: {program}")
    eo_member_set: Set[Member] = eo_monitor.get_all_eo_by_program(program)

    if eo_member_set is None:
        return await interaction.response.send_message(
            "No hay estudiantes orientadores que estén estudiando ese programa :pensive:"
        )

    dept = None
    if program.upper() == "INEL":
        dept = "Ingeniería Eléctrica"
    elif program.upper() == "ICOM":
        dept = "Ingeniería de Computadora"
    elif program.upper() == "INSO":
        dept = "Ingeniería de Software"
    elif program.upper() == "CIIC":
        dept = "Ciencias e Ingeniería de Computación"

    embed = discord.Embed(
        title=f"Estudiantes Orientadores de {program}",
        description=(
            "Aquí están todos los estudiantes orientadores que están "
            f"estudiando {dept} como tu!"
        ),
    )

    for counselor in eo_member_set:
        if counselor is not None:
            embed.add_field(
                name=f"Nombre: {counselor.display_name}",
                value=f"Username: {counselor.name}",
            )

    await interaction.response.send_message(content=None, embed=embed)
