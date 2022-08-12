from typing import Dict, List

import discord
from discord.app_commands import Command


def command(help_list: List[Dict]):
    async def _telephone_guide_help(interaction: discord.Interaction):
        embed = discord.Embed(title="Lista de Contactos disponibles")
        embed.add_field(
            name="Uso",
            value=(
                "Estas son las listas de contactos a los varios departamentos y"
                " facultades en los cuales podrás orientarte."
            ),
        )

        for contact in help_list:
            embed.add_field(
                name=contact["name"],
                value=contact["description"],
            )

        await interaction.response.send_message(embed=embed)

    cmd = Command(
        name="help",
        description="Obtener lista completa de contactos disponibles",
        callback=_telephone_guide_help,
    )

    return cmd
