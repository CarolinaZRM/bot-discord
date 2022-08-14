"""
//  /bot-discord/commands/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/07/11
//
//  Last Modified: Thursday, 11th August 2022 3:14:19 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from discord.app_commands import CommandTree

import log

from . import general as general_commands
from . import leveling_system, server_management, telephone_guide


async def subscribe_slash_commands(cmd_tree: CommandTree):
    try:
        await general_commands.subscribe_commands(cmd_tree)
        await leveling_system.subscribe_commands(cmd_tree)
        await server_management.subscribe_commands(cmd_tree)
        await telephone_guide.subscribe_commands(cmd_tree)
    except Exception as err:
        log.error(err)
