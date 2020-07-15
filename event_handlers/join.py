"""This file is supponsed to contain all the events and commands that are related to member join
"""
import discord
import log
import os


async def event_greet_new_member(client: discord.Client, member: discord.Member):
    # Greets you to server
    await member.send(
        f"*Bienvenido a UPRM y al Discord de TEAM MADE, {member.name}!* :tada: :raised_hands_tone3:\n"
        f"**Por favor, dime cual es tu nombre completo para poder ponerte ese nombre en el servidor y poder asignarte en el grupo que Made eligió para ti!**"
        f"Ejemplo: Fernando J. Bermudez Medina"
    )

    # checks if message was sent by the user and in the DM
    def check_same_user(client_response: discord.Message):
        member_dm_id = member.dm_channel.id
        log.debug(
            f'[DEBUG - join.py | line.17] Client ResponseObj: "{client_response}" ||||| MemberObj: {member}')
        # return true if message belongs to the same member and comes from DM
        return client_response.author == member and client_response.channel.id == member_dm_id

    # Extracts the name of the student from the DM
    name = await client.wait_for("message", check=check_same_user)
    assign_group(client,member,name)
    await member.send("**Gracias!**")

    # Replaces their old name to the one they provided in the DM to the bot
    log.debug(
        f"[VERBOSE - join.py | line.20] {name.author}'s nickname was changed to {name.content}")
    await member.edit(nick=str(name.content))
    await member.send(
        f"Ya todos te veran como: '{name.content}'\n"
        f"Que facil, no?\n"
        "Te digo un secreto :eyes: ... Programar es super divertido y tu tambien puedes hacerlo! :hugging: "
    )

    user_name = name.content

    message_to_send = f'Ahora si me presento formalmente,\n'\
        f"Hola {user_name}!\nMe alegra mucho que estes aqui :tada:\n"\
        "Yo soy *MADE Bot* y sere tu *Bot* Consejero. :smiley:\n"\
        "Estoy aquí para ayudarte con cualquier duda que tengas.\n"\
        "Te puedo ayudar a:\n"\
        "\u2022 Econtrar edificios\n"\
        "\u2022 Información de contacto para algunas oficinas importantes\n"\
        "\u2022 Proveer 'links' muy utiles para tu carrera universitaria.\n"\
        "\u2022 Y muchas cosas más!!!\n\n"\
        "Espero ser de mucha ayuda :thumbsup:\n\n"\
        "Vamos a comenzar por escribir ***!help***.\nEste comando te mostrará la lista de algunas preguntas que me puedes hacer.\nEspero a que lo hagas..."

    await member.send(content=message_to_send)

    # starts waiting block for '!help'
    # checks if user writes !help
    def check_user_writes_help(client_response: discord.Message):
        # return true if message belongs to the same member and message is !help
        return client_response.author == member and client_response.content == '!help'

    await client.wait_for('message', check=check_user_writes_help)
    # wait for the response of the bot
    await client.wait_for('message', check=lambda client_response: client_response.author.bot)
    # finish waiting block

    # starts waiting block for '!contactos'
    #
    message_to_send = f'Eso es {user_name}! :thumbsup: Ahí está la lista de algunos comandos rápidos.\n'\
        'Todavía quedan más comandos con mucha informacion útil para ti :sweat_smile:'\
        'Ahora intenta escribir ***!contactos***, este comando es mas específico y te proveéra una lista de todos los posibles contactos '\
        'que tengo en mi banco de datos. Tratalo ahora :eyes:'
    await member.send(content=message_to_send)

    def check_user_writes_help(client_response: discord.Message):
        # return true if message belongs to the same member and message is !help
        return client_response.author == member and client_response.content == '!contactos'

    await client.wait_for('message', check=check_user_writes_help)
    # wait for the response of the bot
    await client.wait_for('message', check=lambda client_response: client_response.author.bot)
    # finish waiting block

    closing = f"{user_name}, eso es todo por hoy. Ya conoces los dos comandos mas importantes: ***'!help'*** y  ***'!contactos'***\n"\
        'Ya veras que estos te serán muy útiles, despues puedes darme las gracias :sunglasses:\n' \
        'Ahora se te asigno un grupo en especifico de un personaje de Super Smash Bros, lo puedes verificar en tu perfil\n' \
        'El grupo que te toco tiene un canal de texto y de voz para que puedas compartir con los otros miembros de tu grupo\n'\
        'Cualquier inconveniente le puedes escribir a Fernando Bermudez o Gabriel Santiago \n'\
        '¡Hasta luego! Tambien te digo que los Estudiantes Orientadores de Team MADE estan para ayudarte, no dudes en ocuparlos para cualquier duda :grimacing:\n'

    await member.send(content=closing)


def assign_group(client, member, name):
    """
        When a new user enters the server we do the following:
            1) First we iterate through all text files containing all users in all text files that divide users into groups
            2) We try to find said user by their name they provided when they were greeted in each file
            3) If found, we add the role of "prepa" and the role of the group they were assigned
    """
    directory = "directory/of/prepa/lists.txt" #os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # print(os.path.join(directory, filename))
            continue
        else:
            continue