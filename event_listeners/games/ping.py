"""
//  /bot-discord/commands/games/ping.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/13
//
//  Last Modified: Saturday, 13th August 2022 11:11:44 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from discord import Message


async def on_message(message: Message):
    if message.content.lower() == "ping":
        await message.channel.send("Pong :)")
