from discord.channel import ChannelType
from discord.errors import Forbidden
import discord
import log
import os

_ADMIN_CHANNELS = ["counselors", "admins", "general"]
_PREPA_CHANNELS = ["general"]

_CURRENT_DIR = os.path.dirname(__file__)
_TOKEN_FILE = os.path.join(_CURRENT_DIR, "res", "textfiles", 'token.txt')
_ADMINS_FILE = os.path.join(_CURRENT_DIR, "res", "textfiles", 'counselors.txt')
_VALIDATED_COUNSELORS = []

_CLIENT_ID_NUM = 719199208166522881
_GUILD_ID_NUM = 718624993470316554


def readToken():

    f = open(os.path.join(_CURRENT_DIR, _TOKEN_FILE), "r")
    lines = f.readlines()
    return lines[0].strip()


def _extractAdmins(client):
    file_path = os.path.join(_CURRENT_DIR, _ADMINS_FILE)

    file1 = open(file_path, "r")
    f_lines = file1.readlines()

    f_lines = list(map(lambda x: x.strip(), f_lines))
    file1.close()
    current_counselors = set(f_lines)

    guild = client.get_guild(_GUILD_ID_NUM)
    for member in guild.members:
        for role in member.roles:
            if role.name == "@EstudianteOrientador" or role.name == 'studentCounselor':
                current_counselors.add(str(member))

    current_counselors.discard(' ')
    current_counselors.discard('')

    current_counselors = list(current_counselors)
    current_counselors.sort()

    lines2 = '\n'.join(current_counselors)

    file2 = open(file_path, 'w')
    file2.writelines(lines2)
    file2.close()


def _uploadCounselors():
    global _VALIDATED_COUNSELORS
    f = open(os.path.join(_CURRENT_DIR, _ADMINS_FILE), "r")
    for counselor in f:
        _VALIDATED_COUNSELORS.append(counselor.strip())
    f.close()


async def update_admin_list(client: discord.Client):
    _extractAdmins(client)
    _uploadCounselors()
    log.debug('[VERBOSE] Updated Admins.')


async def verify_if_counselor(member: discord.Member):
    log.debug(f"[DEBUG - bot.py] {_VALIDATED_COUNSELORS}")
    if str(member) in _VALIDATED_COUNSELORS:
        log.debug(f'[DEBUG] Joined Member is Counselor: {member}')
        guild: discord.Guild = member.guild
        for role in guild.roles:
            if role.name == '@EstudianteOrientador' or role.name == 'studentCounselor':
                log.debug(f'[DEBUG] Role: {role}')
                try:
                    await member.add_roles(role)
                except Forbidden:
                    log.debug(
                        '[ERROR] Bot does not have permision to add roles.')
    else:
        log.debug(
            f"[DEBUG - bot.py | line.55] Joined user member '{member}' is not Counselor")


def is_sender_counselor(message: discord.Message):
    global _VALIDATED_COUNSELORS
    return str(message.author) in _VALIDATED_COUNSELORS


def is_sender_prepa(message: discord.Message):
    return str(message.author) not in _VALIDATED_COUNSELORS


def is_from_a_channel(message: discord.Message) -> bool:
    if message.channel.type != ChannelType.private:
        log.debug('[_TOKEN_FILE] Is from a chanel')
        return True
    return False


def is_from_dm(message: discord.Message) -> bool:
    if message.channel.type == ChannelType.private:
        log.debug('[_TOKEN_FILE] Is from DM')
        return True
    return False


def is_from_channel(message: discord.Message, channel_name: str) -> bool:
    if message.channel.name == channel_name:
        log.debug('[_TOKEN_FILE] Is from DM')
        return True
    return False
