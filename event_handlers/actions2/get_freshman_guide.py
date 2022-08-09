import os

import discord
import log
from constants import paths
from discord.app_commands import Command

GUIA_PREPISTICA = os.path.join(paths.RESOURCES, "GuiaPrepistica.pdf")


def command():
    log.debug("Guia prep Sub...")
    return Command(
        name="guia_prepistica",
        description="Obtener Guia Prepistica",
        callback=_get_freshman_guide,
    )


async def _get_freshman_guide(interaction: discord.Interaction):
    log.debug("[DEBUG] Entered Freshman Guide")
    await interaction.response.send_message(
        "Aquí esta la guía Prepistica:\n\n",
        file=discord.File(GUIA_PREPISTICA),
    )
