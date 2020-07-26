""""
//
//  prepa.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

This file is suppossed to contain all the events and commands that are only allowed for prepas
"""
import discord
from bot import _GUILD_ID_NUM as ID
import log

inel_counselors = []
icom_counselors = []
cse_counselors = []


def extract_counselors(client: discord.client):
    guild = client.get_guild(ID)
    for member in guild.members:
        for role in member.roles:
            if member is not None:
                if 'INEL' in role.name:
                    log.debug(f"[INEL] Role Found for {member.nick}")
                    inel_counselors.append(member)
                if 'ICOM' in role.name:
                    log.debug(f"[ICOM] Role Found for {member.nick}")
                    icom_counselors.append(member)
                if 'INSO/CIIC' in role.name:
                    log.debug(f"[INSO/CIIC] Role Found for {member.nick}")
                    cse_counselors.append(member)


async def get_counselor_names(message: discord.Message):
    embed = None
    log.debug("[EO] ENTERED COUNSELOR LIST")
    split = message.content.split(":")

    if len(split) == 1 and split[0].upper() == '/EO':
        embed = "No reconozco ese departamento, intenta con *INEL/ICOM/INSO/CIIC*"
        await message.channel.send(embed)
    else:
        if split[0].upper() == "/EO":
            if split[1].upper() == "INEL":
                embed = discord.Embed(title="Estudiantes Orientadores de INEL",
                                      description="Aquí estan todos los estudiantes orientadores que estan estudiando Ingenieria Electrica como tu!")
                for counselor in inel_counselors:
                    if counselor is not None:
                        embed.add_field(
                            name=f"Nombre: {counselor.nick}", value=f"Username: {counselor.name}")
                await message.channel.send(content=None, embed=embed)

            elif split[1].upper() == "ICOM":
                embed = discord.Embed(title="Estudiantes Orientadores de ICOM",
                                      description="Aquí estan todos los estudiantes orientadores que estan estudiando Ingenieria de Computadora como tu!")
                for counselor in icom_counselors:
                    if counselor is not None:
                        embed.add_field(
                            name=f"Nombre: {counselor.nick}", value=f"Username: {counselor.name}")
                await message.channel.send(content=None, embed=embed)

            elif split[1].upper() == "INSO" or split[1].upper() == "CIIC":
                embed = discord.Embed(title="Estudiantes Orientadores de INSO/CIIC",
                                      description="Aquí estan todos los estudiantes orientadores que estan estudiando Ingenieria de Software/Ciencias e Ingenieria de Computacion como tu!")
                for counselor in cse_counselors:
                    if counselor is not None:
                        embed.add_field(
                            name=f"Nombre: {counselor.nick}", value=f"Username: {counselor.name}")
                await message.channel.send(content=None, embed=embed)
