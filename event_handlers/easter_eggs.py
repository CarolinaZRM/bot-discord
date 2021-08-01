'''
//  /event_handlers/easter_eggs.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 07/31/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''

import re
import random

import discord
import log

SHEESH_REGEX = re.compile('s+h+ee+s+h+s*', re.IGNORECASE)

YET_REGEX = re.compile('y+ee+t+s*', re.IGNORECASE)


async def is_sheeshed(message: discord.Message):
    log.debug('[DEBUG] Entered Shheeessh')

    RETURN_SHEESH = 'SHEEEEEEEEEEEEEEEEEEEEEEEEEEEESSSSHHHHHHHHHH :fire:\nOooppss :sweat_smile: Me emocioné jejeje'

    has_sheesh = SHEESH_REGEX.search(message.content)

    if has_sheesh:
        await message.channel.send(content=RETURN_SHEESH)


async def is_yeeted(message: discord.Message):
    log.debug('[DEBUG] Entered Shheeessh')

    RETURN_SHEESH = ['SE YEETIÓ!!!', 'UFFF! YEETIAO jajaja']

    has_yeet = YET_REGEX.search(message.content)

    if has_yeet:
        await message.channel.send(content=random.choice(RETURN_SHEESH))
