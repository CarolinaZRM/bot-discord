"""
//  /handlers/telephone_guide/consejeria_academica.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
from typing import List

import discord
from discord.app_commands import Choice, Command

from .append_fields_to_embed import append_fields_to_embed
from .contacts import asesoria_academica

_PROGRAM = ["icom", "inel", "inso", "ciic"]


def help_data():
    return {
        "name": "asesoria-academica",
        "description": "Contacto de Asesores Académicos y Consejería Profesional para INEL/ICOM/INSO/CIIC",
    }


def command():
    cmd = Command(
        **help_data(),
        callback=_asesoria_academica,
    )

    @cmd.autocomplete(name="program")
    async def autocomplete(_: discord.Interaction, current: str) -> List[Choice[str]]:
        return [
            Choice(name=program.upper(), value=program)
            for program in _PROGRAM
            if current.lower() in program.lower()
        ]

    return cmd


async def _asesoria_academica(interaction: discord.Interaction, program: str):
    program_name = program.lower()
    embed: discord.Embed = None
    if program_name in ("inel", "icom"):
        embed = discord.Embed(title="Asesoria Académica del Departamento de INEL/ICOM")
        ece_cons = asesoria_academica.ECEAsesoriaAcademica()

        append_fields_to_embed(ece_cons, embed)

        embed.remove_field(0)
        embed.insert_field_at(index=0, name="Servicio", value=ece_cons.contact_name)

        embed.add_field(
            name="Sistema de reserva de citas ECE",
            value=ece_cons.appointment_system_link,
        )

        divisor = "\n\u2022 "
        brochure_list = f"\u2022 {divisor.join(ece_cons.brochures)}"
        embed.add_field(name="Folletos Informativos", value=brochure_list)
        embed.add_field(name="Más Información", value=ece_cons.more_info)
        await interaction.response.send_message(embed=embed)
    elif program_name.lower() in ("inso", "ciic"):
        embed = discord.Embed(title="Asesoria Académica del Departamento de INSO/CIIC")
        cse_cons = asesoria_academica.CSEAsesoriaAcademica()

        append_fields_to_embed(cse_cons, embed)

        embed.remove_field(0)
        embed.insert_field_at(index=0, name="Servicio", value=cse_cons.contact_name)

        embed.add_field(
            name="Cuando Puedo Ir al Departamento?",
            value="Cuando quieras! Siempre y cuando Celines o uno de los directores este para atenderte y no estén ocupados",
        )
        divisor = "\n\u2022 "
        # CSE DOESN'T HAVE BROCHURES
        embed.add_field(
            name="CSE Dept. Website", value=cse_cons.brochures[0]  # website link
        )

        embed.add_field(name="Más Información", value=cse_cons.more_info)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            "Los siento, no reconozco ese departamento. :flushed:\n"
            "Intenta con: **INSO, INEL, CIIC o ICOM.**"
        )
