"""
//
//  join.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.
This file is supposed to contain all the events and commands that are related to member join
"""
import csv
from typing import Dict

import discord
from discord import utils
from discord.errors import Forbidden
from constants import paths

try:
    import log
except Exception:
    pass

# Files
_PREPA_FILE = paths.PREPAS.PREPA_LIST


async def event_greet_new_member(client: discord.Client, member: discord.Member):
    # Greets you to server
    await member.send(
        f"*Bienvenido a UPRM y al Discord de TEAM MADE, {member.name}!* :tada: :raised_hands_tone3:\n"
        # f"**Por favor, dime cual es tu username de tu correo institucional para poder asignarte al grupo que Made eligió para ti!**\n"
        # f"Ejemplo: bienvenido.velez"
        f"**Por favor, dime cual es tu correo institucional para poder asignarte al grupo que Made eligió para ti!**\n"
        f"Ejemplo: bienvenido.velez@upr.edu"
    )

    # checks if message was sent by the user and in the DM
    def check_same_user(client_response: discord.Message):
        member_dm_id = member.dm_channel.id
        log.info(
            f'[join.py] Client ResponseObj: "{client_response}" ||||| MemberObj: {member}'
        )
        # return true if message belongs to the same member and comes from DM
        return (
            client_response.author == member
            and client_response.channel.id == member_dm_id
        )

    ##################
    # ask for student number
    student_name = await assign_group(client, member, check_same_user)

    # # Extracts the name of the student from the DM
    # name = await client.wait_for("message", check=check_same_user)

    # await member.send("**Gracias!**")

    # Replaces their old name to the one they provided in the DM to the bot
    log.info(
        f"[VERBOSE - join.py | line.20] {member.name}'s nickname was changed to {student_name}"
    )
    await member.edit(nick=str(student_name))
    await member.send(
        f"Ya todos te verán como: '{student_name}'\n"
        f"Que fácil, no?\n"
        "Te digo un secreto :eyes: ... Programar es super divertido y tu también puedes hacerlo! :hugging: "
    )

    user_name = student_name

    message_to_send = (
        f"Ahora si me presento formalmente,\n"
        f"Hola {user_name}!\nMe alegra mucho que estes aquí :tada:\n"
        "Yo soy *MADE Bot* y sere tu *Bot* Consejero. :smiley:\n"
        "Estoy aquí para ayudarte con cualquier duda que tengas.\n"
        "Te puedo ayudar a:\n"
        "\u2022 Encontrar edificios\n"
        "\u2022 Información de contacto para algunas oficinas importantes\n"
        "\u2022 Proveer 'links' muy útiles para tu carrera universitaria.\n"
        "\u2022 Y muchas cosas más!!!\n\n"
        "Espero ser de mucha ayuda :thumbsup:\n\n"
        "Vamos a comenzar por escribir ***!help***.\nEste comando te mostrará la lista de algunas preguntas que me puedes hacer.\nEspero a que lo hagas..."
    )

    await member.send(content=message_to_send)

    # starts waiting block for '!help'
    # checks if user writes !help
    def check_user_writes_help(client_response: discord.Message):
        # return true if message belongs to the same member and message is !help
        return client_response.author == member and client_response.content == "!help"

    await client.wait_for("message", check=check_user_writes_help)
    # wait for the response of the bot
    await client.wait_for(
        "message", check=lambda client_response: client_response.author.bot
    )
    # finish waiting block

    # starts waiting block for '!contactos'
    #
    message_to_send = (
        f"Eso es {user_name}! :thumbsup: Ahí está la lista de algunos comandos rápidos.\n"
        "Todavía quedan más comandos con mucha información útil para ti :sweat_smile:"
        "Ahora intenta escribir ***!contactos***, este comando es mas específico y te proveéra una lista de todos los posibles contactos "
        "que tengo en mi banco de datos. Trátalo ahora :eyes:"
    )
    await member.send(content=message_to_send)

    def check_user_writes_help(client_response: discord.Message):
        # return true if message belongs to the same member and message is !help
        return (
            client_response.author == member and client_response.content == "!contactos"
        )

    await client.wait_for("message", check=check_user_writes_help)
    # wait for the response of the bot
    await client.wait_for(
        "message", check=lambda client_response: client_response.author.bot
    )
    # finish waiting block

    closing = (
        f"{user_name}, eso es todo por hoy. Ya conoces los dos comandos mas importantes: ***'!help'*** y  ***'!contactos'***\n"
        "Ya veras que estos te serán muy útiles, despues puedes darme las gracias :sunglasses:\n"
        "Ahora se te asigno un grupo en especifico de un personaje de Star Wars, lo puedes verificar en tu perfil\n"
        "El grupo que te toco tiene un canal de texto y de voz para que puedas compartir con los otros miembros de tu grupo\n"
        "Cualquier inconveniente le puedes escribir a Carolina Z. Rodriguez o Gabriel Santiago \n"
        "¡Hasta luego! También te digo que los Estudiantes Orientadores de Team MADE están para ayudarte, no dudes en ocuparlos para cualquier duda :grimacing:\n"
    )

    await member.send(content=closing)


async def assign_group(client: discord.Client, member: discord.Member, check_same_user):
    """
    When a new user enters the server we do the following:
        1) First we iterate through all text files containing all users in all text files that divide users into groups
        2) We try to find said user by their name they provided when they were greeted in each file
        3) If found, we add the role of "prepa" and the role of the group they were assigned
    """
    student_email = await client.wait_for("message", check=check_same_user)

    student_obj = _get_student(student_email.content)

    while student_obj is None:
        await member.send(
            'No encuentro ese email en mis registros. Intenta de nuevo:\n\n***Si tu email no aparece y estas seguro de que eres un prepa de INEL, ICOM, INSO o CIIC, comunicate con cualquier estudiante orientador del servidor de discord. Tienen el rol de "EstudianteOrientador"'
        )
        student_number = await client.wait_for("message", check=check_same_user)
        student_obj = _get_student(student_number.content)

    # el nombre del grupo esta en:
    # student_obj['group id'] o student_obj.get('group id')
    student_group: str = student_obj["group id"]
    student_department: str = student_obj["department"]

    try:
        log.info("{}".format(member.guild.roles))
        group_role = utils.get(member.guild.roles, name=student_group)
        dept_role = utils.get(member.guild.roles, name=student_department.upper())
        prepa_role = utils.get(member.guild.roles, name="prepa")
        log.info(f"Dept: {dept_role}, Group: {group_role}, Prepa: {prepa_role}")
        await member.add_roles(group_role, dept_role, prepa_role)
    except Forbidden:
        log.error(
            f'Bot does not have permission to add roles. Could not add student "{student_obj}" to group.'
        )
        await member.send(
            "No pude asignarte a un grupo. Contacta a algún estudiante orientador e informarle de este error."
        )

    return "{} {} {}".format(
        student_obj["first name"],
        student_obj["middle initial"],
        student_obj["last names"],
    )


def _get_student(student_number: str) -> Dict[str, str]:
    with open(_PREPA_FILE) as teams_list_file:
        rows = csv.DictReader(teams_list_file, delimiter=",")
        for row in rows:
            if (
                student_number.split("@")[0].lower()
                == row["student email"].split("@")[0]
            ):
                log.debug(
                    f"""[ASSIGN] Username found: {row['student email'].split("@")[0]} for student {"{} {} {}".format(row["first name"], row["middle initial"], row["last names"])}"""
                )
                return dict(row)
    return None


async def made(member: discord.Member):
    if member.id == 719645695484756008:
        log.info("[MADE] Made has joined server")
        await member.add_roles("ConsejeraProfesional", "admin", "DCSP")
    else:
        log.info("[MADE] Made has not joined server")


if __name__ == "__main__":
    pass
