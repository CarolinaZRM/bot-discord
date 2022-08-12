""""
//
//  prepa.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

This file is supposed to contain all the events and commands that are only allowed for prepas
"""
import discord

import config
import log

inel_counselors = set()
icom_counselors = set()
cse_counselors = set()
inso_counselors = set()


def extract_counselors(client: discord.client):
    guild = client.get_guild(int(config.GUILD_ID_NUM))
    # @TODO: REMEMBER TO ALWAYS KEEP GUILD ID NUM UPDATED WHEN SWITCHING FROM SERVER TO SERVER
    # 'id' value is EO role id
    eo = discord.Role(
        data={"id": 989729347004923913, "name": "@EstudianteOrientador"},
        guild=guild,
        state=None,
    )
    for member in guild.members:
        for role in member.roles:
            if member is not None and eo in member.roles:
                if "INEL" in role.name:
                    log.info(f"[INEL] Role Found for {member.nick}")
                    inel_counselors.add(member)
                if "ICOM" in role.name:
                    log.info(f"[ICOM] Role Found for {member.nick}")
                    icom_counselors.add(member)
                if "CIIC" in role.name:
                    log.info(f"[CIIC] Role Found for {member.nick}")
                    cse_counselors.add(member)
                if "INSO" in role.name:
                    log.info(f"[INSO] Role Found for {member.nick}")
                    inso_counselors.add(member)


async def get_counselor_names(message: discord.Message):
    embed = None
    log.info("[EO] ENTERED COUNSELOR LIST")
    split = message.content.split(":")

    if (
        split[0].upper() == "!EO"
        and split[1].upper() != "INEL"
        and split[1].upper() != "ICOM"
        and split[1].upper() != "INSO"
        and split[1].upper() != "CIIC"
    ):
        embed = "No reconozco ese departamento, intenta con *INEL/ICOM/INSO/CIIC*"
        await message.channel.send(embed)
    else:
        if split[0].upper() == "!EO":
            if split[1].upper() == "INEL":
                embed = discord.Embed(
                    title="Estudiantes Orientadores de INEL",
                    description=(
                        "Aquí están todos los estudiantes orientadores que están"
                        " estudiando Ingeniería Electrica como tu!"
                    ),
                )
                for counselor in inel_counselors:
                    if counselor is not None:
                        # @TODO: Fix
                        if (
                            counselor.name == "Arianys Martínez Fuentes"
                        ):  # hardcode because Ariany's username is her actual name
                            embed.add_field(
                                name=f"Nombre: {counselor.display_name}",
                                value=f"Username: {counselor.name}",
                            )
                        else:
                            embed.add_field(
                                name=f"Nombre: {counselor.nick}",
                                value=f"Username: {counselor.name}",
                            )
                await message.channel.send(content=None, embed=embed)

            elif split[1].upper() == "ICOM":
                embed = discord.Embed(
                    title="Estudiantes Orientadores de ICOM",
                    description=(
                        "Aquí están todos los estudiantes orientadores que están"
                        " estudiando Ingeniería de Computadora como tu!"
                    ),
                )
                for counselor in icom_counselors:
                    if counselor is not None:
                        embed.add_field(
                            name=f"Nombre: {counselor.nick}",
                            value=f"Username: {counselor.name}",
                        )
                await message.channel.send(content=None, embed=embed)

            elif split[1].upper() == "INSO":
                embed = discord.Embed(
                    title="Estudiantes Orientadores de INSO",
                    description=(
                        "Aquí están todos los estudiantes orientadores que están"
                        " estudiando Ingeniería de Software como tu!"
                    ),
                )
                for counselor in inso_counselors:
                    if counselor is not None:
                        embed.add_field(
                            name=f"Nombre: {counselor.nick}",
                            value=f"Username: {counselor.name}",
                        )
                await message.channel.send(content=None, embed=embed)

            elif split[1].upper() == "CIIC":
                embed = discord.Embed(
                    title="Estudiantes Orientadores de CIIC",
                    description=(
                        "Aquí están todos los estudiantes orientadores que están"
                        " estudiando Ciencias e Ingeniería de Computación como tu!"
                    ),
                )
                for counselor in cse_counselors:
                    if counselor is not None:
                        embed.add_field(
                            name=f"Nombre: {counselor.nick}",
                            value=f"Username: {counselor.name}",
                        )
                await message.channel.send(content=None, embed=embed)
