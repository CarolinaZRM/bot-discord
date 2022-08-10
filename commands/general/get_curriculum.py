"""
//  /home/gbrl18/bot-discord/commands/general/get_curriculum.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/10
//  
//  Last Modified: Wednesday, 10th August 2022 7:04:43 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import os
from typing import List

import discord
from constants import paths
from discord.app_commands import Command, Choice

from commands.utils.autocomplete import program_autocomplete

# PDF Files
_CURRICULOS_MAP = {
    "INEL": os.path.join(paths.CURRICULOS, "INEL.pdf"),
    "INSO": os.path.join(paths.CURRICULOS, "INSO.pdf"),
    "CIIC": os.path.join(paths.CURRICULOS, "CIIC.pdf"),
    "ICOM": os.path.join(paths.CURRICULOS, "ICOM.pdf"),
}

_PROG_NAME_MAP = {
    "INEL": "Electrical Engineering",
    "ICOM": "Computer Engineering",
    "INSO": "Software Engineering",
    "CIIC": "Computer Science & Engineering",
}


def command():
    cmd = Command(
        name="curriculo",
        description="PDF del currículo del Programa de Estudio",
        callback=_get_curriculum,
    )

    cmd.autocomplete(name="program")(program_autocomplete)

    return cmd


async def _get_curriculum(interaction: discord.Interaction, program: str):

    if not program or len(program) == 0:
        await interaction.response.send_message(
            "No me dijiste que currículo necesitas :slight_frown:\nIntenta con: INEL/ICOM/INSO/CIIC"
        )
    else:
        if program not in _CURRICULOS_MAP:
            return await interaction.response.send_message(
                f"Disculpa los inconvenientes, pero no tengo el Currículo para el programa de {program}"
            )

        await interaction.response.send_message(
            f"Here is the {_PROG_NAME_MAP[program]} Curriculum:"
        )
        await interaction.followup.send(file=discord.File(_CURRICULOS_MAP[program]))
