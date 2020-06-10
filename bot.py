import discord
from discord.channel import ChannelType
import log
import os

ADMIN_CHANNELS = ["counselors", "admins", "general"]
PREPA_CHANNELS = ["general"]

CURRENT_DIR = os.path.dirname(__file__)
ADMINS_FILE = os.path.join(CURRENT_DIR, "res", "textfiles", 'counselors.txt')
VALIDATED_USERS = []
DEBUG = True


CLIENT_ID_NUM = 718911269813485568
GUILD_ID_NUM = 718624993470316554


def extractAdmins(client):
    f = open(os.path.join(CURRENT_DIR, ADMINS_FILE), "w")
    guild = client.get_guild(GUILD_ID_NUM)
    for member in guild.members:
        for role in member.roles:
            if role.name == "@EstudianteOrientador":
                f.write(str(member) + '\n')
    f.close()


def validateAdmins():
    global VALIDATED_USERS
    file = open(os.path.join(CURRENT_DIR, ADMINS_FILE), "r")
    for counselor in file:
        VALIDATED_USERS.append(counselor.rstrip())
    file.close()


def update_admin_list(client: discord.Client):
    extractAdmins(client)
    validateAdmins()
    log.debug('[VERBOSE] Updated Admins.')


def is_sender_admin(message: discord.Message):
    global VALIDATED_USERS
    return str(message.author) in VALIDATED_USERS


def is_sender_prepa(message: discord.Message):
    return str(message.author) not in VALIDATED_USERS


def is_from_a_channel(message: discord.Message) -> bool:
    log.debug(f'advad {message.channel.type}')
    log.debug(f'advad {ChannelType.group}')
    if message.channel.type != ChannelType.private:
        log.debug('[DEBUG] Is from a chanel')
        return True
    return False


def is_from_dm(message: discord.Message) -> bool:
    if message.channel.type == ChannelType.private:
        log.debug('[DEBUG] Is from DM')
        return True
    return False


def is_from_channel(message: discord.Message, channel_name: str) -> bool:
    if message.channel.name == channel_name:
        log.debug('[DEBUG] Is from DM')
        return True
    return False
