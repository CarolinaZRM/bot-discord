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


async def subscribe_easter_eggs(message: discord.Message):
    await _is_sheeshed(message)
    await _is_yeeted(message)
    await _do_parkour(message)


async def _is_sheeshed(message: discord.Message):
    log.debug('[DEBUG] Entered Shheeessh')

    RETURN_SHEESH = [
        'Sheeeshhss :eyes:',
        'SHEEEEEEEEEEEEEEEEEEEEEEEEEEEESSSSHHHHHHHHHH :fire:\nOooppss :sweat_smile: Me emocioné jejeje'
    ]

    has_sheesh = SHEESH_REGEX.search(message.content)

    if has_sheesh:
        await message.reply(content=random.choice(RETURN_SHEESH))


async def _is_yeeted(message: discord.Message):
    log.debug('[DEBUG] Entered Shheeessh')

    RETURN_SHEESH = ['SE YEETIÓ!!!', 'UFFF! YEETIAO jajaja']

    has_yeet = YET_REGEX.search(message.content)

    if has_yeet:
        await message.reply(content=random.choice(RETURN_SHEESH))


PARKOUR_GIFS = ['https://tenor.com/view/parkour-theoffice-freerunning-gif-5128248',
                'https://tenor.com/view/parkour-the-office-andy-bernard-gif-11765843']

PARKOUR_RESPONSE = ['YAASSSS', 'Of course!!! :sunglasses:']


async def _do_parkour(message: discord.Message):
    CMD = r'(do)? *you *(do|know) *parkour *\?*'

    user_input = message.content.lower()

    # if does not start with "bot" or contains a BOT Tag, terminate
    if not (re.match(r'^(bot).*', user_input) or re.search(r'(<@!719199208166522881>).*', user_input)):
        return

    # if contains the question, return GIF
    if re.search(CMD, user_input):
        await message.reply(content=f'{random.choice(PARKOUR_RESPONSE)}\n{random.choice(PARKOUR_GIFS)}')
