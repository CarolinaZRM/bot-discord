"""
//  /bot-discord/commands/server_management/user_count.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/09
//  
//  Last Modified: Tuesday, 9th August 2022 10:16:06 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

from discord.app_commands import Command

from discord import Interaction


def command():
    return Command(
        name="user-count",
        description="Get user count in this channel",
        callback=_user_count,
    )


async def _user_count(interaction: Interaction):
    await interaction.response.defer(thinking=False)
    if interaction.channel is not None:
        member_count = len(interaction.channel.members)
        await interaction.response.send_message(
            f"Number of Members: {member_count}", ephemeral=True
        )
