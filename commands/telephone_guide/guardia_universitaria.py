"""
//  /handlers/telephone_guide/guardia_universitaria.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
from code import interact
import discord
from discord.app_commands import Command

from .contacts import servicios
from .append_fields_to_embed import append_fields_to_embed


def help_data():
    return {
        "name": "guardia-univ",
        "description": "Información de contacto de la guardia Universitaria",
    }


def command():
    return Command(**help_data(), callback=_guardia_universitaria_contact)


async def _guardia_universitaria_contact(interaction: discord.Interaction):
    guardia = servicios.GuardiaUniversitaria()
    embed = discord.Embed(
        title="Info Guardia Universitaria", description="Información Rápida"
    )

    embed = append_fields_to_embed(guardia, embed)

    divisor = "\n\u2022 "
    additional_info_list = f"\u2022 {divisor.join(guardia.additional_helpful_info)}"
    embed.add_field(name="Más Información Utíl", value=additional_info_list)
    embed.add_field(name="Enlaces Útiles", value=guardia.more_info_link)

    await interaction.response.send_message(embed=embed)
