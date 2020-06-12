"""This file is supponsed to contain all the events and commands that are related to member join
"""
import discord
import log


async def event_greet_new_member(client: discord.Client, member: discord.Member):
    # Greets you to server
    await member.send(
        f"*Bienvenido a UPRM y al Discord de TEAM MADE, {member.name}!* :tada: :smiley: :raised_hands_tone3:\n"
        f"**Por favor, dime cual es tu nombre completeo para poder ponerte ese nombre en el servidor!**"
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

    await member.send("**Gracias!**")

    # Replaces their old name to the one they provided in the DM to the bot
    log.debug(
        f"[VERBOSE - join.py | line.20] {name.author}'s nickname was changed to {name.content}")
    await member.edit(nick=str(name.content))
    await member.send(
        f"Ya todos te veran como: '{name.content}'\n"
        f"Que facil, no? :thinking:\n"
        "Te digo un secreto :eyes: ... Programar es super divertido y tu tambien puedes hacerlo! :hugging: "
    )
