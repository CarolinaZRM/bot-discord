import log
from discord.app_commands import CommandTree

from . import general as general_commands
from . import server_management, telephone_guide


async def subscribe_slash_commands(cmd_tree: CommandTree):
    try:
        await general_commands.subscribe_commands(cmd_tree)
        await telephone_guide.subscribe_commands(cmd_tree)
        await server_management.subscribe_commands(cmd_tree)
        await cmd_tree.sync()
    except Exception as err:
        log.error(err)
