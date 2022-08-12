"""
// /bot-discord/commands/telephone_guide/asesoria_academica.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2021/06/23
//
//  Last Modified: Wednesday, 10th August 2022 7:25:21 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import discord
from discord.app_commands import Command

from commands.utils.autocomplete import program_autocomplete

from .append_fields_to_embed import append_fields_to_embed
from .contacts import asesoria_academica


def help_data():
    return {
        "name": "asesoria-academica",
        "description": (
            "Contacto de Asesores Académicos y Consejería Profesional para"
            " INEL/ICOM/INSO/CIIC"
        ),
    }


def command():
    cmd = Command(
        **help_data(),
        callback=_asesoria_academica,
    )

    cmd.autocomplete(name="program")(program_autocomplete)

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
            value=(
                "Cuando quieras! Siempre y cuando Celines o uno de los directores este"
                " para atenderte y no estén ocupados"
            ),
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
