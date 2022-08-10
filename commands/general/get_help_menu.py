import bot
from controllers import help_menu
from discord import Embed, Interaction
from discord.app_commands import Command


def command():
    return Command(name="help", description="Menu de ayuda", callback=_help_menu)


async def _help_menu(interaction: Interaction):
    msg_author = interaction.user

    if bot.is_sender_counselor(msg_author):
        help_menu_embed = help_menu.help_menu_for_counselor()
    elif bot.is_sender_prepa(msg_author):
        help_menu_embed = help_menu.help_menu_for_prepa()
    else:
        help_menu_embed = help_menu.help_menu_base()

    await interaction.response.send_message(content=None, embed=help_menu_embed)
