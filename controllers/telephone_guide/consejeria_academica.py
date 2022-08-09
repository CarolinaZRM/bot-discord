'''
//  /handlers/telephone_guide/consejeria_academica.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import discord

from .contacts import consejeria_profesional
from .generate_embed import generate_embed


def get_consejeria_academica(sections):
    if len(sections) <= 1:
        return 'Por favor, especifica abreviación del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!consejeroacad:inel"'

    dept_name = sections[1]
    embed: discord.Embed = None
    if dept_name.lower() in ('inel', 'icom'):
        embed = discord.Embed(
            title='Consejeria Académica del Departamento de INEL/ICOM')
        ece_cons = consejeria_profesional.ECEConsejerosProfesional()

        generate_embed(ece_cons, embed)

        embed.remove_field(0)
        embed.insert_field_at(
            index=0,
            name='Servicio',
            value=ece_cons.contact_name
        )

        embed.add_field(
            name='Sistema de reserva de citas ECE',
            value=ece_cons.appointment_system_link
        )
        divisor = '\n\u2022 '
        brochure_list = f'\u2022 {divisor.join(ece_cons.brochures)}'
        embed.add_field(
            name='Folletos Informativos',
            value=brochure_list
        )

        embed.add_field(
            name='Más Información',
            value=ece_cons.more_info
        )
    elif dept_name.lower() in ('inso', 'ciic'):
        embed = discord.Embed(
            title='Consejeria Académica del Departamento de INSO/CIIC')
        cse_cons = consejeria_profesional.CSEConsejerosProfesional()

        generate_embed(cse_cons, embed)

        embed.remove_field(0)
        embed.insert_field_at(
            index=0,
            name='Servicio',
            value=cse_cons.contact_name
        )

        embed.add_field(
            name='Cuando Puedo Ir al Departamento?',
            value="Cuando quieras! Siempre y cuando Celines o uno de los directores este para atenderte y no estén ocupados"
        )
        divisor = '\n\u2022 '
        # CSE DOESN'T HAVE BROCHURES
        embed.add_field(
            name='CSE Dept. Website',
            value=cse_cons.brochures[0]  # website link
        )

        embed.add_field(
            name='Más Información',
            value=cse_cons.more_info
        )
    else:
        return 'Los siento, no reconozco ese departamento. :flushed:\n'\
            'Intenta con: **INSO, INEL, CIIC o ICOM.**'

    return embed
