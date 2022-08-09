'''
//  /handlers/telephone_guide/get_asistencia_econ.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import discord

from .generate_embed import generate_embed
from .contacts import servicios


def get_asistencia_econ(section):
    asis_econ = servicios.AsistenciaEconomica()

    return_message = "Esta es la información de la Oficina de Asistencia Económica:\n\n"

    embed = discord.Embed(title='Info Asistencia Económica',
                          description='Información Rapida')

    generate_embed(asis_econ, embed)
    embed = embed.add_field(name='Fechas Importantes (Prestamos, Beca, etc.)',
                            value=asis_econ.important_dates_link, inline=True)

    return {
        'embed': embed,
        'content_first': return_message
    }
