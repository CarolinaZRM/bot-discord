"""
//  /bot-discord/commands/server_management/__init__.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/09
//  
//  Last Modified: Thursday, 11th August 2022 3:14:35 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""


import log
from constants import roles
from discord import Interaction
from discord.app_commands import CommandTree, Group, MissingAnyRole, MissingRole

from . import attendance, user_count, bulk_delete_admin

from commands.utils.command_group import InteractionCheckedGroup


async def subscribe_commands(command_tree: CommandTree = None):
    log.info("subscribing Server Management Commands...")

    COMMAND_NAME = "server_management"

    async def dm_interaction_check(self, interaction: Interaction) -> bool:
        if not hasattr(interaction.user, "roles"):
            # call from DM
            await interaction.response.send_message(
                "Este commando no se puede utilizar desde el DM"
            )
            return False

        for role in interaction.user.roles:
            if role.name in roles.ADMINISTRATOR_ROLES:
                return True
        raise MissingAnyRole(list(roles.ADMINISTRATOR_ROLES))

    server_management_grp = InteractionCheckedGroup(
        name=COMMAND_NAME,
        description=f"Comandos para EOs y Admin para manejo y metadata del Servidor",
    )

    server_management_grp.set_interaction_check(dm_interaction_check)

    @server_management_grp.error
    async def on_group_error(interaction: Interaction, error: Exception):
        log.info(error)
        if isinstance(error, MissingAnyRole) or isinstance(error, MissingRole):
            await interaction.response.send_message(
                "No tienes el rol para poder usar este commando", ephemeral=True
            )

    # Add commands to group
    server_management_grp.add_command(attendance.command())
    server_management_grp.add_command(user_count.command())
    server_management_grp.add_command(bulk_delete_admin.command())

    # Add group to RootTree
    command_tree.add_command(server_management_grp)

    log.info("Finished subscribing...")


__all__ = [
    subscribe_commands,
]
