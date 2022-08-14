"""
//  /bot-discord/commands/games/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/13
//
//  Last Modified: Saturday, 13th August 2022 11:08:14 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from discord import Client, Message

from . import guess_game, ping, rock_paper_scissors


async def on_message(message: Message, client: Client):
    await ping.on_message(message)
    await guess_game.on_message(message, client)
    await rock_paper_scissors.on_message(message, client)
