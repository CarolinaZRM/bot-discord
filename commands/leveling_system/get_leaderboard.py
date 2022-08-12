"""
// /bot-discord/commands/leveling_system/get_leaderboard.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/11
//
//  Last Modified: Thursday, 11th August 2022 4:35:32 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from typing import Any, Dict

from discord import Embed, Interaction
from discord.app_commands import Command

from controllers.leveling_system import general_leaderboard


def command():
    return Command(
        name="leaderboard",
        description="Get leaderboard",
        callback=_leaderboard,
    )


async def _leaderboard(interaction: Interaction):
    top_peeps = general_leaderboard()
    top_peeps_text = []

    for position, user_info in enumerate(top_peeps):
        user_info: Dict[str, Any]
        # add 1 to position to make the index start from 1
        top_peeps_text.append(
            f"{position + 1} - <@!{user_info.get('user_id')}>\t|\tLevel:"
            f" {user_info.get('level')}"
        )

    print(top_peeps_text)

    embed = Embed(title=":trophy: Leaderboard :trophy:", color=11901259)

    embed.add_field(name="Crewmates", value="\n".join(top_peeps_text), inline=False)

    await interaction.response.send_message(embed=embed)
