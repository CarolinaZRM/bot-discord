"""
//  /handlers/telephone_guide/get_asistencia_econ.py
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

__RETURN_MESSAGE = "Esta es la información de la Oficina de Asistencia Económica:\n\n"

__EMBED = None


def __init_embed():
    global __EMBED

    asistencia_econ = servicios.AsistenciaEconomica()

    __EMBED = discord.Embed(
        title="Info Asistencia Económica", description="Información Rápida"
    )

    append_fields_to_embed(asistencia_econ, __EMBED)

    __EMBED.add_field(
        name="Fechas Importantes (Prestamos, Beca, etc.)",
        value=asistencia_econ.important_dates_link,
        inline=True,
    )


__init_embed()


def help_data():
    return {
        "name": "asistencia-econ",
        "description": "Información de Contacto de Asistencia Económica",
    }


def command():
    return Command(
        **help_data(),
        callback=_get_asistencia_econ,
    )


async def _get_asistencia_econ(interaction: discord.Interaction):
    if not __EMBED:
        __init_embed()

    await interaction.response.send_message(content=__RETURN_MESSAGE, embed=__EMBED)
