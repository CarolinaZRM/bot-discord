"""
//
//  bot.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Edited by Gabriel Santiago on June 20, 2021
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
import discord
from discord.channel import ChannelType
from discord.errors import Forbidden

from constants import admins, paths
import config
import log
import os
import youtube_dl

os.makedirs(os.path.join(paths.AUDIO), exist_ok=True)

_COUNSELOR_USERS_FILE = os.path.join(paths.TEXT_FILES, 'counselors.txt')

_VALIDATED_COUNSELORS = []

_TMP_AUDIO_FILE = os.path.join(paths.AUDIO, "song.mp3")


class __MusicPlayerState(object):
    # Player state variables
    USER_PLAYING_MUSIC = None
    PLAYING = False
    CURRENT_USER_PLAYING_MUSIC = None


def _extractAdmins(client: discord.Client):
    counselor_file_ref = open(_COUNSELOR_USERS_FILE, "r")

    counselor_user_handles = set(
        map(lambda x: x.strip(),
            counselor_file_ref.readlines()))

    counselor_file_ref.close()

    guild = client.get_guild(config.GUILD_ID_NUM)
    for member in guild.members:
        for role in member.roles:
            if role.name == "@EstudianteOrientador" \
                    or role.name == 'ConsejeraProfesional':
                counselor_user_handles.add(str(member))

    counselor_user_handles.discard(' ')
    counselor_user_handles.discard('')

    current_counselors = list(counselor_user_handles)
    current_counselors.sort()

    updated_handle_list = '\n'.join(current_counselors)

    file2 = open(_COUNSELOR_USERS_FILE, 'w')
    file2.writelines(updated_handle_list)
    file2.close()


def _uploadCounselors():
    global _VALIDATED_COUNSELORS
    f = open(_COUNSELOR_USERS_FILE, "r")
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
            if role.name == '@EstudianteOrientador' \
                    or role.name == 'ConsejeraProfesional':
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
    return message.author.id in admins.ADMIN_IDS


def is_from_a_channel(message: discord.Message) -> bool:
    if message.channel.type != ChannelType.private:
        log.debug('[MESSAGE] Is from a chanel')
        return True
    return False


def is_from_dm(message: discord.Message) -> bool:
    if message.channel.type == ChannelType.private:
        log.debug('[MESSAGE] Is from DM')
        return True
    return False


def is_from_channel(message: discord.Message, channel_name: str) -> bool:
    if message.channel.name == channel_name:
        log.debug('[MESSAGE] Is from DM')
        return True
    return False


async def set_streaming(client: discord.Client, message: discord.Message):
    user_message = message.content

    if user_message == '!botstartstream' \
            and is_sender_counselor(message) \
            and is_from_dm(message):
        sender: discord.User = message.author

        # checks if message was sent by the user and in the DM
        def check_same_user(client_response: discord.Message):
            sender_dm_id = sender.dm_channel.id
            return client_response.author == sender \
                and client_response.channel.id == sender_dm_id

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

        await client.wait_for('message', check=check_same_user)

        await client.change_presence(activity=None)


async def join_voice_channel(client: discord.Client, message: discord.Message):
    if message.content == "!join":
        if not is_sender_counselor(message):
            log.debug(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command {message.content}")
            await message.author.send(f"{message.author.nick}, no tienes los permisos para usar este comando")
            return

        if not hasattr(message.author, 'voice'):
            await message.author.send('No puedes unirme a un canal de voz desde el DM')
            return

        user_name = None

        if hasattr(message.author, 'nick'):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_state: discord.VoiceState = message.author.voice
        log.debug(f'[DEBUG - Author Voice State] {voice_state}')
        if not voice_state:
            await message.author.send(f"Hola {user_name}, primero te tienes que conectar tu al canal de voz para yo saber a cual quieres que me conecte")
            return

        voice_channel: discord.VoiceChannel = voice_state.channel

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild)

        # verify ownreship of music streaming
        if __MusicPlayerState.USER_PLAYING_MUSIC is None:
            # add ownership is no one has it
            __MusicPlayerState.USER_PLAYING_MUSIC = user_name
        elif __MusicPlayerState.USER_PLAYING_MUSIC != user_name:
            # no eres quien hizo el join original
            await message.author.send(f"Hola {user_name}, no tienes la autorización para unirme a el canal **'{voice_channel}'**. **{__MusicPlayerState.USER_PLAYING_MUSIC}** tiene control del bot streamer.")
            return

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(voice_channel)
            print(f"The bot has moved to {voice_channel}")
        else:
            await voice_channel.connect()

        await message.author.send(f'Ya me uni al canal de voz: {voice_channel}')


async def leave_voice_channel(client: discord.Client, message: discord.Message):
    if message.content == "!leave":
        if not is_sender_counselor(message):
            log.debug(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command {message.content}")
            await message.author.send(f"{message.author.nick}, no tienes los permisos para usar este comando")
            return

        if not hasattr(message.author, 'voice'):
            await message.author.send('No me puedes sacar a un canal de voz desde el DM')
            return

        user_name = None

        if hasattr(message.author, 'nick'):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_state: discord.VoiceState = message.author.voice
        log.debug(f'[DEBUG - Author Voice State] {voice_state}')
        if not voice_state:
            await message.author.send(f"Hola {user_name}, primero te tienes que conectar tu al canal de voz"
                                      "para yo saber de cual quieres que me desconecte")
            return

        voice_channel: discord.VoiceChannel = voice_state.channel

        log.debug(f"[DEBUG] {client.voice_clients}")

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild)

        if not voice_client or voice_client.channel != voice_channel:
            await message.author.send(f"No estoy conectado al canal: {voice_channel}")
            return

        # verify ownreship of music streaming
        if __MusicPlayerState.USER_PLAYING_MUSIC != user_name:
            # no eres quien hizo el join original
            await message.author.send(f"Hola {user_name}, no tienes la autorización para removerme del canal **'{voice_channel}'**. **{__MusicPlayerState.USER_PLAYING_MUSIC}** tiene control del bot streamer.")
            return
        else:
            # clean ownership of music streaming
            __MusicPlayerState.USER_PLAYING_MUSIC = None

        if voice_client.is_connected():
            await voice_client.disconnect()
            await message.author.send(f'Ya me desconecté del canal de voz: {voice_channel}')


async def play_audio(client: discord.Client, message: discord.Message):
    sections = message.content.split(' ')

    if sections[0] != "!play":
        return

    if __MusicPlayerState.PLAYING:
        if __MusicPlayerState.CURRENT_USER_PLAYING_MUSIC != message.author:

            return

    if not is_sender_counselor(message):
        log.debug(
            f"[PREPA_BREACH] user {message.author.nick} tried to to command {message.content}")
        await message.author.send(f"{message.author.nick}, no tienes los permisos para usar este comando")
        return

    if not hasattr(message.author, 'voice'):
        await message.author.send('No puedes unirme a un canal de voz desde el DM')
        return

    user_name = None

    if hasattr(message.author, 'nick'):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    if len(sections) < 2:
        await message.author.send(f"{user_name}, te falto el URL del video o cancion. Puede ser de cualquier website publico. (Youtube, Soundcloud, etc.)")
        return

    url = sections[1]

    global _TMP_AUDIO_FILE

    try:
        if os.path.isfile(_TMP_AUDIO_FILE):
            os.remove(_TMP_AUDIO_FILE)
    except PermissionError:
        await message.author.send('No puedo dar play a otra cancion. Un audio esta en play.\nPonlo en pausa.')
        return

    voice_client: discord.VoiceClient = discord.utils.get(
        client.voice_clients, guild=message.guild)

    if not voice_client:
        await message.author.send("No estoy conectado a ningún canal de voz")
        return

    if voice_client.is_playing():
        await message.author.send('No puedo darle PLAY a un audio mientras uno esta en PLAY. Intenta pausar el audio primero')
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(paths.AUDIO, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

    except youtube_dl.DownloadError as err:
        print(f'[ERROR] {err}')
        await message.author.send(f'Me econtre con un error descargando el video.\n'
                                  f"Error:\n{str(err)}")
        return

    name = ""
    for file in os.listdir(os.path.join(paths.AUDIO)):
        if file.endswith(".mp3"):
            name = file
            os.rename(os.path.join(paths.AUDIO, file), _TMP_AUDIO_FILE)

    voice_client.play(discord.FFmpegPCMAudio(_TMP_AUDIO_FILE))
    name = name \
        .replace('.mp3', '') \
        .rsplit('-', 2)

    await message.author.send(f"{user_name}, ya **'{name} '** esta en PLAY")


async def pause_audio(client: discord.Client, message: discord.Message):
    if message.content == "!pause":

        if not is_sender_counselor(message):
            log.debug(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command {message.content}")
            await message.author.send(f"{message.author.nick}, no tienes los permisos para usar este comando")
            return

        if not hasattr(message.author, 'voice'):
            await message.author.send('No puedes pausar a un canal de voz desde el DM')
            return

        user_name = None

        if hasattr(message.author, 'nick'):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild)

        if not voice_client:
            await message.author.send(f"{user_name}, No estoy conectado a ningún canal de voz")
            return

        voice_channel: discord.VoiceChannel = voice_client.channel

        if voice_client.is_playing():
            voice_client.pause()
            await message.author.send(f'Pausado en el canal {voice_channel}')


async def resume_audio(client: discord.Client, message: discord.Message):
    if message.content == "!resume":
        if not is_sender_counselor(message):
            log.debug(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command {message.content}")
            await message.author.send(f"{message.author.nick}, no tienes los permisos para usar este comando")
            return

        if not hasattr(message.author, 'voice'):
            await message.author.send('No puedes pausar a un canal de voz desde el DM')
            return

        user_name = None

        if hasattr(message.author, 'nick'):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild)

        if not voice_client:
            await message.author.send(f"${user_name}, No estoy conectado a ningún canal de voz")
            return

        voice_channel: discord.VoiceChannel = voice_client.channel

        if voice_client.is_paused():
            voice_client.resume()
            await message.author.send(f'Resumido en el canal {voice_channel}')
