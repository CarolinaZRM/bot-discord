"""
//  /handlers/telephone_guide/get_dept_info.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

import discord
from discord.app_commands import Command

from commands.utils.autocomplete import program_autocomplete

from .append_fields_to_embed import append_fields_to_embed
from .contacts import departamentos


def help_data():
    return {
        "name": "department",
        "description": (
            "Información de contacto de los departamentos de INEL/ICOM/INSO/CIIC"
        ),
    }


def command():
    cmd = Command(
        **help_data(),
        callback=_dept_contact,
    )

    cmd.autocomplete("program")(program_autocomplete)

    return cmd


async def _dept_contact(interaction: discord.Interaction, program: str):
    program_name: str = program.lower()

    embed = None
    if program_name in ("inso", "ciic"):
        cse = departamentos.CSEDepartment()
        embed = discord.Embed(
            title="Información del departamento de CSE",
            description="Información Utíl de CSE",
        )

        append_fields_to_embed(cse, embed)
        await interaction.response.send_message(embed=embed)
    elif program_name in ("icom", "inel"):
        ece = departamentos.ECEDepartment()
        embed = discord.Embed(
            title="Información del departamento de ECE",
            description="Información Utíl de ECE",
        )
        append_fields_to_embed(ece, embed)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            "No reconozco ese departamento :eyes: :confused:\n"
            "Intenta con: INEL, ICOM, INSO o CIIC"
        )
