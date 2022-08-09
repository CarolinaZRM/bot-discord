'''
//  /handlers/telephone_guide/dept_cons_psicologicos.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import discord

from .contacts import servicios
from .generate_embed import generate_embed


def get_dept_cons_psicologicos(sections):
    embed = discord.Embed(
        title='Información de Departamento de Consejería y Servicios Psicológicos (DCSP)')
    dcsp = servicios.ConsejeriaServiciosPsicologicos()
    generate_embed(dcsp, embed)
    embed.add_field(
        name='Pagina Oficial',
        value=dcsp.official_website
    )

    divisor = '\n\u2022 '
    links_list = f'\u2022 {divisor.join(dcsp.enlaces_rapidos)}'
    embed.add_field(
        name='Enlaces Rápidos',
        value=links_list
    )
    embed.add_field(
        name='Contactanos',
        value=dcsp.contatanos
    )

    content_response = dcsp.mensaje_muy_importante
    return {
        'embed': embed,
        'content': content_response
    }
