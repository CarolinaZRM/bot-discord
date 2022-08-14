"""
//  /bot-discord/listeners/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/13
//
//  Last Modified: Saturday, 13th August 2022 11:45:50 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

from discord import Client, Message

from . import games


async def on_message(message: Message, client: Client):
    await games.on_message(message, client)
