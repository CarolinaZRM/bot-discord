"""
//  /bot-discord/controllers/eo_monitor/load_into_memory.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 6:08:02 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from collections import defaultdict
from typing import Set, Union

from discord import Client, Member, utils

import config
import log
from constants import roles

__EOS_BY_PROGRAM = defaultdict(set)


__PROGRAMS = ["INEL", "ICOM", "INSO", "CIIC"]


def get_all_eo_by_program(program: str) -> Union[Set[Member], None]:
    return __EOS_BY_PROGRAM.get(program, None)


def add_eo_by_program(program: str, counselor: Member) -> None:
    __EOS_BY_PROGRAM[program].add(counselor)
    log.debug(__EOS_BY_PROGRAM)


def load_eo_into_memory(client: Client) -> None:
    guild = client.get_guild(int(config.GUILD_ID_NUM))

    eo_role = utils.get(guild.roles, name=roles.ESTUDIANTE_ORIENTADOR)

    for member in guild.members:
        for role in member.roles:
            if member is not None and eo_role in member.roles:
                if role.name in __PROGRAMS:
                    __EOS_BY_PROGRAM[role.name].add(member)

    log.debug(f"EOs by Program {__EOS_BY_PROGRAM}")
