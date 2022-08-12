"""
//  /bot-discord/commands/server_management/attendance.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/07/11
//
//  Last Modified: Tuesday, 9th August 2022 10:16:48 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""


import collections
import csv
import os
import re
import shutil
from curses.ascii import isdigit
from datetime import datetime
from os import path

import discord
from discord.app_commands import Command

import log
from constants import paths as app_paths

ATTENDANCE_PATH = path.join(app_paths.TEXT_FILES, "attendance")

try:
    os.mkdir(ATTENDANCE_PATH)
except OSError:
    # directory already exists
    # delete directory, contents not needed, memory waste
    shutil.rmtree(ATTENDANCE_PATH)
    os.mkdir(ATTENDANCE_PATH)


def command():
    return Command(
        name="attendance", description="Get attendance", callback=_get_attendance
    )


async def _get_attendance(interaction: discord.Interaction, channel_id: str):
    if not str.isdigit(channel_id):
        return await interaction.response.send_message(
            f"El *channel_id*:<{channel_id}> provisto es invalido",
            ephemeral=True,
        )

    await interaction.response.defer(thinking=False)

    response_method = interaction.user

    server: discord.Guild = interaction.guild

    if server is None:
        return await response_method.send(
            "Este medio no pertenece a ningún ***SERVER***.\nEste commando solo puede"
            " ser utilizado desde un servidor, no DM.\n\nDisculpa :confused:"
        )

    target_channel_id = channel_id
    target_channel_obj = server.get_channel(int(target_channel_id))

    if not target_channel_obj:
        return await response_method.send(
            f"El *channel_id* <{target_channel_id}> provisto no es valido para el"
            f' servidor, ***"{server}"***.\nIntenta de nuevo con otro ID, o contacta al'
            " **BOT DEV TEAM**"
        )

    members_in_attendance = []
    for idx, member in enumerate(target_channel_obj.members):
        member_roles = filter(
            lambda role: role != "@everyone", [role.name for role in member.roles]
        )

        member_tuple = (
            idx + 1,
            getattr(member, "nick", member.name),
            "|".join(member_roles),
        )

        members_in_attendance.append(member_tuple)

    now = datetime.now()  # current date and time
    formatted_datetime = now.strftime("%Y%m%d-%H%M%S")

    list_file_path = _attendance_list(
        members_in_attendance, formatted_datetime, server, target_channel_obj
    )
    stats_file_path, roles_count = _attendance_stats(
        members_in_attendance, formatted_datetime, server, target_channel_obj
    )

    stats_embed = _generate_stats_embed(roles_count, server, target_channel_obj)

    await response_method.send(
        content=(
            "Hola aca te paso las estadísticas de asistencia para"
            f" **{target_channel_obj}**"
        ),
        embed=stats_embed,
    )
    await response_method.send(
        content=f'**Archivo con la lista de asistencia para "{target_channel_obj}"**',
        file=discord.File(list_file_path),
    )
    await response_method.send(
        content=(
            f'**Archivo con las estadísticas de asistencia para "{target_channel_obj}"**'
        ),
        file=discord.File(stats_file_path),
    )

    __delete_file_safe(list_file_path)
    __delete_file_safe(stats_file_path)


def __delete_file_safe(abs_path):
    try:
        os.unlink(abs_path)
    except OSError:
        pass


def _generate_stats_embed(roles_count: dict, server, channel):
    embed = discord.Embed(
        title="Estadísticas de Asistencias",
        description=f"**Server**: {server}\n**Canal**: {channel}",
        colour=discord.colour.Colour.green(),
        timestamp=datetime.now(),
    )

    roles_text = []

    for role, qty in sorted(roles_count.items()):
        roles_text.append(f"{role}  =>  {qty}")

    if len(roles_text) == 0:
        roles_text.append("\u2022 **No hay nadie en este canal al momento**")

    embed.add_field(name="Roles y Cantidad", value="\n".join(roles_text), inline=False)

    return embed


def _attendance_list(members_in_attendance, formatted_datetime, server, channel):
    server_name = str(server).replace(" ", "-").replace(".", "")
    channel_name = str(channel).replace(" ", "-").replace(".", "")
    file_name = f"attendance-{server_name}-{channel_name}-{formatted_datetime}.csv"

    abs_path = path.join(ATTENDANCE_PATH, file_name)

    with open(abs_path, "w") as attendance_file:
        #  Create instance of CSV Writer
        wtr = csv.writer(attendance_file)

        # Create csv header
        wtr.writerow(["ID", "Nickname/Account Username", "Lista de roles"])

        #  Save members list to CSV
        for connected_member in members_in_attendance:
            wtr.writerow([str(i) for i in connected_member])

    return abs_path


def _attendance_stats(members_in_attendance, formatted_datetime, server, channel):
    server_name = str(server).replace(" ", "-").replace(".", "")
    channel_name = str(channel).replace(" ", "-").replace(".", "")
    file_name = f"attendance-stats-{server_name}-{channel_name}-{formatted_datetime}.csv"

    member_roles_count = collections.defaultdict(int)

    for member in members_in_attendance:
        # in position 3 of the members list is the roles list separated by "|"
        if len(member[2]) == 0:
            member_roles_count["No assigned yet"] += 1
            continue

        member_roles = member[2].split("|")

        for role in member_roles:
            member_roles_count[role] += 1

    abs_path = path.join(ATTENDANCE_PATH, file_name)
    # save into stats file
    with open(abs_path, "w") as stats_file:
        writer = csv.writer(stats_file)
        writer.writerow(["ID", "Role Name", "Quantity of members with role"])
        for idx, item in enumerate(sorted(member_roles_count.items())):
            writer.writerow([idx + 1, item[0], item[1]])

    return abs_path, member_roles_count
