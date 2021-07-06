'''
//  /handlers/telephone_guide/get_dept_info.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import discord

from .contacts import departamentos
from .generate_embed import generate_embed


def get_dept_info(sections):

    if len(sections) <= 1:
        return 'Por favor, especifica abreviación del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!dept:inso"'

    department_name: str = sections[1].lower()

    embed = None
    if department_name in ('inso', 'ciic'):
        cse = departamentos.CSEDepartment()
        embed = discord.Embed(title="Información del departamento de CSE",
                              description="Información Utíl de CSE")

        return generate_embed(cse, embed)

    elif department_name in ('icom', 'inel'):
        ece = departamentos.ECEDepartment()
        embed = discord.Embed(title="Información del departamento de ECE",
                              description="Información Utíl de ECE")
        return generate_embed(ece, embed)

    else:
        embed = "No reconozco ese departamento :eyes: :confused:\n"\
            "Intenta con: INEL, ICOM, INSO o CIIC"

    return embed
