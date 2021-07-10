"""
//
//  daily_logs.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
import json
import os
from datetime import datetime, timezone

import discord
from constants import paths

_LOG_DIR = os.path.join(paths.TEXT_FILES, "logs")
_FILE_PATH = None


def _init_logs():
    global _FILE_PATH
    current_time = datetime.now(timezone.utc).strftime("%Y%m%d")
    os.makedirs(_LOG_DIR, exist_ok=True)
    _FILE_PATH = os.path.join(_LOG_DIR, f"{current_time}.log")


_init_logs()


def getRoles(member: discord.Member):
    if not hasattr(member, 'roles'):
        return 'Received from DM'
    return [str(role.name) for role in member.roles]


def analytics(message: discord.Message):
    user_message = message.content
    if len(user_message) > 0 \
            and user_message[0] in ("/", '!', '?') \
            and not message.author.bot:
        with open(_FILE_PATH, 'a+') as log_file:
            log_data = {
                'timestamp': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'command': user_message,
                'roles': getRoles(message.author),
                'author': str(message.author)
            }
            log_file.write(f'{json.dumps(log_data)}\n')
