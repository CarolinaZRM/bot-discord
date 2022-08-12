"""
// /bot-discord/commands/leveling_system/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/11
//
//  Last Modified: Thursday, 11th August 2022 4:30:07 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from discord import Interaction
from discord.app_commands import AppCommandError, CommandTree, NoPrivateMessage

import log
from commands.utils.command_group import InteractionCheckedGroup

from . import get_leaderboard, get_level_status


async def subscribe_commands(command_tree: CommandTree = None):
    log.info("subscribing Leveling System Commands...")

    grp = InteractionCheckedGroup(name="levels", description="Leveling system")

    async def check_if_dm(interaction: Interaction):
        if not hasattr(interaction.user, "roles"):
            # Called from DM, not allowed
            await interaction.response.send_message(
                "Este commando no se puede utilizar desde el DM"
            )
            raise NoPrivateMessage("Hi")
        return True

    grp.set_interaction_check(check_if_dm)

    @grp.error
    async def _on_error(_: Interaction, error: AppCommandError):
        if isinstance(error, NoPrivateMessage):
            pass
        else:
            log.error(error)

    grp.add_command(get_leaderboard.command())
    grp.add_command(get_level_status.command())

    command_tree.add_command(grp)
