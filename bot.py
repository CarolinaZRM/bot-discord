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


def is_sender_admin(message: discord.Message):
    return message.author.id == 539112744553676812 or message.author.id == 541298986535878677


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


async def set_streaming(client: discord.Client, message: discord.Message):
    user_message = message.content

    if user_message == '!botstartstream' and is_sender_counselor(message) and is_from_dm(message):
        sender: discord.User = message.author

        # checks if message was sent by the user and in the DM
        def check_same_user(client_response: discord.Message):
            sender_dm_id = sender.dm_channel.id
            return client_response.author == sender and client_response.channel.id == sender_dm_id

        await sender.send(content='Cual va a ser el nombre de la actividad?')
        activity_name = await client.wait_for('message', check=check_same_user)
        activity_name = activity_name.content

        await sender.send(content="Escribe el link del video para 'stream':")
        activity_url = await client.wait_for('message', check=check_same_user)
        activity_url = activity_url.content

        await client.change_presence(activity=discord.Activity(
            name=activity_name,
            url=activity_url,
            type=discord.ActivityType.streaming,
            state='Watching',
            details=f'Viewing {activity_name}'
        ))

        # checks if message was sent by the user and in the DM
        def check_same_user_stop_streaming(client_response: discord.Message):
            sender_dm_id = sender.dm_channel.id
            return client_response.author == sender \
                and client_response.channel.id == sender_dm_id \
                and client_response.content == '!botstopstream'

        await client.wait_for('message', check=check_same_user)

        await client.change_presence(activity=None)


async def join_voice_channel(message: discord.Message):
    if message.content != '!join':
        return

    voice_state: discord.VoiceState = message.author.voice
    log.debug(f'[DEBUG - Author Voice State] {voice_state}')
    if not voice_state:
        await message.author.send(f"Hola {message.author.name}, primero te tienes que conectar tu al canal de voz"
                                  "para yo saber a cual quieres que me conecte")
        return

    voice_channel: discord.VoiceChannel = voice_state.channel

    try:
        voice_client: discord.VoiceClient = await voice_channel.connect()
    except discord.ClientException:
        await message.author.send(f'Ya estoy connectado al canal de voz: {voice_channel}')
        return

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(voice_channel)
    else:
        voice = await voice_client.connect()

    await message.author.send(f'Ya me uni al canal de voz: {voice_channel}')


async def leave_voice_channel(client: discord.Client, message: discord.Message):
    if message.content != '!leave':
        return

    voice_state: discord.VoiceState = message.author.voice
    log.debug(f'[DEBUG - Author Voice State] {voice_state}')
    if not voice_state:
        await message.author.send(f"Hola {message.author.name}, primero te tienes que conectar tu al canal de voz"
                                  "para yo saber de cual quieres que me desconecte")
        return

    voice_channel: discord.VoiceChannel = voice_state.channel

    log.debug(f"[DEBUG] {client.voice_clients}")

    voice_client: discord.VoiceClient = discord.utils.get(
        client.voice_clients, guild=message.guild)

    if not voice_client:
        await message.author.send(f"No estoy conectado al canal: {voice_channel}")

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await message.author.send(f'Ya me desconecté del canal de voz: {voice_channel}')
