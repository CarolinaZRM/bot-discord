"""
// /bot-discord/commands/utils/program_autocomplete.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/10
//
//  Last Modified: Wednesday, 10th August 2022 7:18:45 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

from typing import List

import discord
from discord.app_commands import Choice

_PROG_NAME_MAP = {
    "INEL": "INEL - Electrical Engineering",
    "ICOM": "ICOM - Computer Engineering",
    "INSO": "INSO - Software Engineering",
    "CIIC": "CIIC - Computer Science & Engineering",
}


async def program_autocomplete(
    _: discord.Interaction, current: str
) -> List[Choice[str]]:
    return [
        Choice(name=program_name, value=abbreviation)
        for abbreviation, program_name in _PROG_NAME_MAP.items()
        if current.upper() in program_name
    ]
