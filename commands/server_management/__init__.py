"""
//  /commands/server_management/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 08/09/2022
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""


import log
from constants import roles
from discord import Interaction
from discord.app_commands import CommandTree, Group, MissingAnyRole

from . import attendance, user_count


async def subscribe_commands(command_tree: CommandTree = None):
    log.info("subscribing Server Management Commands...")

    COMMAND_NAME = "server_management"

    server_management_grp = Group(
        name=COMMAND_NAME,
        description=f"Comandos para EOs y Admin para manejo y metadata del Servidor",
    )

    @server_management_grp.interaction_check
    def __auth(interaction: Interaction):
        for role in interaction.user.roles:
            if role.name in roles.ADMINISTRATOR_ROLES:
                return True
        raise MissingAnyRole(list(roles.ADMINISTRATOR_ROLES))

    @server_management_grp.error
    async def __on_group_error(interaction: Interaction, error: Exception):
        log.info(error)
        if isinstance(error, MissingAnyRole):
            await interaction.response.send_message(
                "No tienes el rol para poder usar este commando", ephemeral=True
            )

    # Add commands to group
    server_management_grp.add_command(attendance.command())
    server_management_grp.add_command(user_count.command())

    # Add group to RootTree
    command_tree.add_command(server_management_grp)

    log.info("Finished subscribing...")


__all__ = [
    subscribe_commands,
]
