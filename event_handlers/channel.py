"""
//
//  channel.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""

import discord
import bot
import log


async def event_user_count(message: discord.Message):
    log.debug('[VERBOSE] Entered User count')
    if "!user-count" == message.content.lower():
        log.debug('[DEBUG] Contains user-count')
        if bot.is_from_a_channel(message):
            member_count = len(message.guild.members)
            await message.channel.send(f"""Number of Members: {member_count}""")
