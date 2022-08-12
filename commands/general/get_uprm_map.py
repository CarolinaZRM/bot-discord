import discord
from discord.app_commands import Command

import log


def command():
    return Command(
        name="map",
        description="Provee un enlace a el Mapa de UPRM",
        callback=_get_uprm_map,
    )


async def _get_uprm_map(interaction: discord.Interaction):
    log.info("Entered UPRM MAP")

    embed = discord.Embed(
        title="Mapa - Recinto Universitario de Mayagüez",
        description=(
            "Enlace al Mapa de RUM con marcas y localizaciones de los edificios"
            " principales."
        ),
        url="https://www.uprm.edu/portales/mapa/",
        colour=discord.colour.Colour.green(),
        type="link",
    )

    await interaction.response.send_message(embed=embed)
