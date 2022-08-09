import log
from discord.app_commands import CommandTree

from . import (
    get_academic_calendar,
    get_faq,
    get_freshman_guide,
    get_help_menu,
    get_rules,
    get_student_orgs,
    get_uprm_map,
)


async def subscribe_commands(command_tree: CommandTree = None):
    log.info("subscribing...")
    try:
        command_tree.add_command(get_academic_calendar.command())
        command_tree.add_command(get_faq.command())
        command_tree.add_command(get_freshman_guide.command())
        command_tree.add_command(get_help_menu.command())
        command_tree.add_command(get_rules.command())
        command_tree.add_command(get_student_orgs.command())
        command_tree.add_command(get_uprm_map.command())
    except Exception as e:
        print(e)

    log.info("Finished subscribing...")
