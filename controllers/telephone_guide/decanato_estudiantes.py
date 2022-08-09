'''
//  /handlers/telephone_guide/decanato_estudiantes.py
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


def get_decanato_estudiante(sections):
    embed = discord.Embed(
        title='Información de Departamento del Decanato de Estudiantes')
    decanato = servicios.DecanatoEstudiantes()
    generate_embed(decanato, embed)
    embed.add_field(
        name='Pagina Web',
        value=decanato.website
    )

    divisor = "\n\u2022 "
    social_media_list = f'\u2022 {divisor.join(decanato.social_media)}'
    embed.add_field(
        name="Redes Sociales",
        value=social_media_list
    )

    return embed
