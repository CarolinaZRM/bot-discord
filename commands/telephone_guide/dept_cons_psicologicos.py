"""
//  /handlers/telephone_guide/dept_cons_psicologicos.py
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
        "name": "dcsp",
        "description": (
            "Información del Departamento de Consejería y Servicios Psicológicos (DCSP)"
        ),
    }


def command():
    return Command(
        **help_data(),
        callback=_dept_cons_psicologicos,
    )


_EMBED = None
_CONTENT_RESPONSE = None


def __init_embed():
    global _EMBED, _CONTENT_RESPONSE
    _EMBED = discord.Embed(
        title="Información de Departamento de Consejería y Servicios Psicológicos (DCSP)"
    )
    dcsp = servicios.ConsejeriaServiciosPsicologicos()
    append_fields_to_embed(dcsp, _EMBED)
    _EMBED.add_field(name="Pagina Oficial", value=dcsp.official_website)

    divisor = "\n\u2022 "
    links_list = f"\u2022 {divisor.join(dcsp.enlaces_rapidos)}"
    _EMBED.add_field(name="Enlaces Rápidos", value=links_list)
    _EMBED.add_field(name="Contactanos", value=dcsp.contatanos)

    _CONTENT_RESPONSE = dcsp.mensaje_muy_importante


async def _dept_cons_psicologicos(interaction: discord.Interaction):
    if not _EMBED:
        __init_embed()

    await interaction.response.send_message(
        embed=_EMBED,
    )
    await interaction.followup.send(_CONTENT_RESPONSE)
