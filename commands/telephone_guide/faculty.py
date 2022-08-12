"""
// /bot-discord/commands/telephone_guide/faculty.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2021/06/23
//  
//  Last Modified: Wednesday, 10th August 2022 7:27:01 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import discord
from commands.utils.autocomplete import program_autocomplete
from discord.app_commands import Command

_CSE_FACULTY = {
    "Bienvenido Velez Rivera": "Acting Dean of Engineering\nFull Time Professor\nbienvenido.velez@upr.edu",
    "Emmanuel Arzuaga Cruz": "Associate Director\nFull Time Professor\nearzuaga@ece.uprm.edu",
    "Heidy Sierra Gil": "Associate Professor\nheidy.sierra1@upr.edu",
    "Jose L. Melendez": "Special Assistant to the Chancellor\nFull Time Professor\njose.melendez37@upr.edu",
    "Kejie Lu": "Full Time Professor\nkejie.lu@upr.edu",
    "Manuel Rodriguez Martinez": "Full Time Professor\nmanuel.rodriguez7@upr.edu",
    "Marko Schütz Schmuck": "Full Time Professor\nmarko.schutz@upr.edu",
    "Pedro I. Rivera Vega": "Acting CSE Director\nFull Time Professor\np.rivera@upr.edu",
    "Wilson Rivera Gallego": "Full Time Professor\nwilson.riveragallego@upr.edu",
}

_ECE_FACULTY = {
    "Gerson Beauchamp": "Full Time Professor\ngerson.beauchamp@upr.edu",
    "Guillermo Serrano": "Full Time Professor\nguillermo.serrano.@upr.edu",
    "Hamed Parsiani Gobadi": "Full Time Professor\nhamed.parsiani@upr.edu",
    "Henrick Ierick": "Full Time Professor\nhenrick.ierick@upr.edu",
    "Isidoro Couvertier": "Full Time Professor\nisidoro.couvertiero@upr.edu",
    "Jose Cedeño": "Full Time Professor\njose.cedeno3@upr.edu",
    "Manuel Jimenez": "Full Time Professor\nmanuel.jimenez@upr.edu",
    "Nayda Santiago Santiago": "Full Time Professor\nnayda.santiago@upr.edu",
    "Rogelio Palomera ": "Full Time Professor\nrogelio.palomera@upr.edu",
    "Shawn David Hunt": "Full Time Professor\nshawndavid.hunt@upr.edu",
}


def help_data():
    return {
        "name": "faculty",
        "description": "Contacto de la facultad de los departamentos de INEL/ICOM/INSO/CIIC",
    }


def command():
    cmd = Command(**help_data(), callback=_faculty_contact_info)

    cmd.autocomplete(name="program")(program_autocomplete)

    return cmd


_ECE_EMBED = None
_CSE_EMBED = None


def __init_ece():
    global _ECE_EMBED
    _ECE_EMBED = discord.Embed(title="Facultad ECE", description="")

    _ECE_EMBED.add_field(
        name="Para más contactos de Facultad",
        value="https://ece.uprm.edu/people/faculty/#cn-top",
    )
    for name, role in _ECE_FACULTY.items():
        _ECE_EMBED.add_field(name=name, value=role)


def __init_cse():
    global _CSE_EMBED
    _CSE_EMBED = discord.Embed(title="Facultad CSE", description="")
    _CSE_EMBED.add_field(
        name="Para más contactos de Facultad",
        value="https://www.uprm.edu/cse/faculty/",
    )
    for name, role in _CSE_FACULTY.items():
        _CSE_EMBED.add_field(name=name, value=role)


async def _faculty_contact_info(interaction: discord.Interaction, program: str):
    program_name: str = program.lower()
    embed = None
    if program_name in ("inso", "ciic"):
        if not _CSE_EMBED:
            __init_cse()
        embed = _CSE_EMBED

    elif program_name in ("inel", "icom"):
        if not _ECE_EMBED:
            __init_ece()
        embed = _ECE_EMBED
    else:
        return await interaction.response.send_message(
            "No reconozco ese departamento :eyes: :confused:\n"
            "Intenta con: INEL, ICOM, INSO o CIIC"
        )

    await interaction.response.send_message(embed=embed)
