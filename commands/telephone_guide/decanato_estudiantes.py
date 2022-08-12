"""
//  /handlers/telephone_guide/decanato_estudiantes.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
import discord
from discord.app_commands import Command

from .append_fields_to_embed import append_fields_to_embed
from .contacts import servicios


def help_data():
    return {
        "name": "decanato-estudiantes",
        "description": "Información de contacto de Decanato de Estudiantes",
    }


def command():
    return Command(
        **help_data(),
        callback=_decanato_estudiante,
    )


async def _decanato_estudiante(interactions: discord.Interaction):
    embed = discord.Embed(
        title="Información de Departamento del Decanato de Estudiantes"
    )
    decanato = servicios.DecanatoEstudiantes()
    append_fields_to_embed(decanato, embed)
    embed.add_field(name="Pagina Web", value=decanato.website)

    divisor = "\n\u2022 "
    social_media_list = f"\u2022 {divisor.join(decanato.social_media)}"

    embed.add_field(name="Redes Sociales", value=social_media_list)

    await interactions.response.send_message(embed=embed)
