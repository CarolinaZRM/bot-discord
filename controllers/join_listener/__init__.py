"""
//  /home/gbrl18/bot-discord/controllers/join_listener/__init__.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/11
//  
//  Last Modified: Thursday, 11th August 2022 9:27:28 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Edited by Fernando Bermudez June 10, 2020
//
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from copy import copy
from typing import Dict, Union

import discord
from constants import roles
from db import get_database
from discord import utils
from discord.errors import Forbidden

try:
    import log
except Exception:
    pass


async def event_greet_new_member(client: discord.Client, member: discord.Member):
    log.info(
        f"User joined | ${member} ${member.display_name} ${member.name}${member.discriminator}"
    )

    # Greets you to server
    await member.send(
        f"*Bienvenido a UPRM y al Discord de TEAM MADE, {member.name}!* :tada: :raised_hands_tone3:\n"
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
    # ask for student email
    student_email: discord.Message = await client.wait_for(
        "message", check=check_same_user
    )

    student_info: Union[Dict[str, str], None] = _get_student_info(student_email.content)

    while student_info is None:
        await member.send(
            'No encuentro ese email en mis registros. Intenta de nuevo:\n\n***Si tu email no aparece y estas seguro de que eres un prepa de INEL, ICOM, INSO o CIIC, comunícate con cualquier estudiante orientador del servidor de discord. Tienen el rol de "EstudianteOrientador"'
        )
        student_email = await client.wait_for("message", check=check_same_user)
        student_info = get_student_info(student_email.content)

    await assign_group(member, student_info["group_id"], student_info["department_id"])

    student_full_name = f"{student_info['first_name']} {student_info['middle_initial'] or ''} {student_info['last_name']}"
    if student_info["mother_lastname"]:
        student_full_name += f" {student_info['mother_lastname']}"

    # Replaces their old name to the one they provided in the DM to the bot
    log.debug(
        f"join_listener.greet {member.name}'s nickname was changed to {student_full_name}"
    )

    await member.edit(nick=str(student_full_name))
    await member.send(
        f"Ya todos te verán como: '{student_full_name}'\n"
        f"Que fácil, no?\n"
        "Te digo un secreto :eyes: ... Programar es super divertido y tu también puedes hacerlo! :hugging: "
    )

    user_name = student_full_name
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
        "Ya veras que estos te serán muy útiles, después puedes darme las gracias :sunglasses:\n"
        "Ahora se te asigno un grupo en especifico de un personaje de Star Wars, lo puedes verificar en tu perfil\n"
        "El grupo que te toco tiene un canal de texto y de voz para que puedas compartir con los otros miembros de tu grupo\n"
        "Cualquier inconveniente le puedes escribir a Carolina Z. Rodriguez o Gabriel Santiago \n"
        "¡Hasta luego! También te digo que los Estudiantes Orientadores de Team MADE están para ayudarte, no dudes en ocuparlos para cualquier duda :grimacing:\n"
    )

    await member.send(content=closing)


async def assign_group(member: discord.Member, group_name: str, department_name: str):
    try:
        log.debug(f"Previous roles for user: {member} | {member.guild.roles}")
        group_role = utils.get(member.guild.roles, name=group_name)
        dept_role = utils.get(member.guild.roles, name=department_name.upper())
        prepa_role = utils.get(member.guild.roles, name="prepa")
        log.debug(f"Dept: {dept_role}, Group: {group_role}, Prepa: {prepa_role}")
        await member.add_roles(group_role, dept_role, prepa_role)
    except Forbidden:
        log.error(
            f'Bot does not have permission to add roles. Could not add student "{member}" to group.'
        )
        await member.send(
            "No pude asignarte a un grupo. Contacta a algún estudiante orientador e informarle de este error."
        )

    return True


def _get_student_info(student_email: str) -> Union[Dict[str, str], None]:
    internal_email = copy(student_email)

    if not student_email.endswith("@upr.edu"):
        internal_email = internal_email.split("@")[0]
        internal_email += "@upr.edu"

    student_data = (
        get_database().get_collection("prepas").find_one({"email": internal_email})
    )

    if not student_data:
        log.info(f"_get_student_info: Student UPR EMAIL not found: {student_email}")
        return None

    return student_data


async def assign_roles_to_made(member: discord.Member) -> bool:
    if member.id == 719645695484756008:
        log.info("[MADE] Made has joined server")
        roles_to_add = []
        for role_name in roles.MADE_ROLES:
            role_obj = utils.get(member.guild.roles, name=role_name)
            if not role_obj:
                role_obj = member.guild.create_role(name=role_name)
            roles_to_add.append(role_obj)
        await member.add_roles(*roles_to_add)
        return True
    return False


async def on_join(member: discord.Member, client: discord.Client):
    is_made = await assign_roles_to_made(member)
    if not is_made:
        await event_greet_new_member(client, member)


__all__ = ["on_join"]
