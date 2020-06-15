import discord, log
import os.path as path
from datetime import (datetime as dt, date)

_CURRENT_DIR = path.dirname("DUMMY LOG.txt")
_LOG_DIR = path.join(_CURRENT_DIR, "res", "textfiles", "logs")

def getRoles(member : discord.Member):
    roles = []
    for role in member.roles:
        roles.append(str(role.name))
    return roles

async def analytics(message : discord.Message):

    log_file = None
    log.debug(f"""[LOG] LOGGING MESSAGE SENT BY {message.author} ON {dt.now()} """)
    PATH = path.join(_LOG_DIR, f"{date.today()}.txt")
    if not path.exists(PATH):
        log_file = open(PATH, "w")
    else:
        log_file = open(PATH,"a")

    roles = getRoles(message.author)
    if "!" in message.content or "/" in message.content or "?" in message.content:
        log_file.write(f"""[{dt.now()}] MESSAGE: {message.content}, TYPE: command, AUTHOR: {message.author}, ROLES: {", ".join(roles)} \n""")
    else:
        log_file.write(f"""[{dt.now()}] MESSAGE: {message.content}, TYPE: mesage, AUTHOR: {message.author}, ROLES: {", ".join(roles)} \n""")

    log_file.close()


