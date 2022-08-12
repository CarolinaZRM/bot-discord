"""
//  /bot-discord/controllers/admin_monitor/listeners.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 4:23:15 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import discord
from discord import Role, utils
from discord.errors import Forbidden

import config
import log
from constants import roles

from .cache import add_eo_by_program, load_eo_into_memory
from .dao import add_user_to_eo, get_student_orientator, update_eo_list


async def on_member_join(member: discord.Member):
    if get_student_orientator(str(member)):
        eo_role: discord.Role = utils.get(
            member.guild.roles, name=roles.ESTUDIANTE_ORIENTADOR
        )
        try:
            await member.add_roles(eo_role)
            add_eo_by_program(member)
        except Forbidden:
            log.error("Bot does not have permission to add roles.")


async def on_member_update(before: discord.Member, after: discord.Member):
    log.debug(f"Updating member: before: {before} after: {after}")
    if before.roles == after.roles:
        return

    eo_role: discord.Role = utils.get(after.roles, name=roles.ESTUDIANTE_ORIENTADOR)
    if eo_role:
        add_user_to_eo(str(after))
        log.debug(f"Member {str(after)} updated. Roles: {after.roles}")
        for role in after.roles:
            role: Role
            if role and role.name in roles.PROGRAM_ROLES:
                add_eo_by_program(after, role.name)


async def on_ready(client: discord.Client):
    list_of_registered_eos = []
    for member in client.get_guild(int(config.GUILD_ID_NUM)).members:
        eo_role = utils.get(member.roles, name=roles.ESTUDIANTE_ORIENTADOR)
        if not eo_role:
            continue
        list_of_registered_eos.append(str(member))
    update_eo_list(list_of_registered_eos)
    load_eo_into_memory(client)
