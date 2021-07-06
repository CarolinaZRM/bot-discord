'''
//  /handlers/telephone_guide/guardia_universitaria.py
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


def get_guardia_universitaria(section):
    guardia = servicios.GuardiaUniversitaria()
    embed = discord.Embed(title='Info Guardia Universitaria',
                          description='Información Rapida')

    embed = generate_embed(guardia, embed)

    divisor = '\n\u2022 '
    additional_info_list = f"\u2022 {divisor.join(guardia.additional_helpful_info)}"
    embed.add_field(name="Más Información Utíl", value=additional_info_list)
    embed.add_field(name="Enlaces Útiles", value=guardia.more_info_link)

    return embed
