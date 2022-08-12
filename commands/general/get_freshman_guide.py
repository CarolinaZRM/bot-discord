import os

import discord
from discord.app_commands import Command

import log
from constants import paths

GUIA_PREPISTICA = os.path.join(paths.RESOURCES, "GuiaPrepistica.pdf")


def command():
    log.info("Guia prep Sub...")
    return Command(
        name="guia_prepistica",
        description="Obtener Guia Prepistica",
        callback=_get_freshman_guide,
    )


async def _get_freshman_guide(interaction: discord.Interaction):
    log.info("Entered Freshman Guide")
    await interaction.response.send_message(
        "Aquí esta la guía Prepistica:\n\n",
        file=discord.File(GUIA_PREPISTICA),
    )
