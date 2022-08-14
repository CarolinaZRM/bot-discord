"""
//
//  bot.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Edited by Gabriel Santiago on June 20, 2021
//  Edited by Orlando Saldaña on July 23, 2021
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
import os
from typing import Union

import discord
import youtube_dl
from discord.channel import ChannelType

import log
from constants import paths, roles

os.makedirs(os.path.join(paths.AUDIO), exist_ok=True)


_TMP_AUDIO_FILE = os.path.join(paths.AUDIO, "song.mp3")


class __MusicPlayerState(object):
    # Player state variables
    USER_PLAYING_MUSIC = None
    PLAYING = False
    CURRENT_USER_PLAYING_MUSIC = None


def is_sender_counselor(author: Union[discord.Member, discord.User]):
    if isinstance(author, discord.User):
        return False

    eo_role = discord.utils.get(author.roles, name=roles.ESTUDIANTE_ORIENTADOR)

    return eo_role is not None


def is_sender_prepa(author: Union[discord.Member, discord.User]):
    if isinstance(author, discord.User):
        return False

    prepa_role = discord.utils.get(author.roles, name=roles.PREPA)

    return prepa_role is not None


def is_sender_admin(author: Union[discord.Member, discord.User]):
    if isinstance(author, discord.User):
        return False

    admin_role = discord.utils.find(
        lambda role: role.name in roles.ADMINISTRATOR_ROLES, author.roles
    )

    return admin_role is not None


def is_from_a_channel(message: discord.Message) -> bool:
    if message.channel.type != ChannelType.private:
        log.info("[MESSAGE] Is from a chanel")
        return True
    return False


def is_from_dm(message: discord.Message) -> bool:
    if message.channel.type == ChannelType.private:
        log.info("[MESSAGE] Is from DM")
        return True
    return False


def is_from_channel(message: discord.Message, channel_name: str) -> bool:
    if message.channel.name == channel_name:
        log.info("[MESSAGE] Is from DM")
        return True
    return False


# This is a command method
async def set_streaming(client: discord.Client, message: discord.Message):
    user_message = message.content

    if (
        user_message == "!botstartstream"
        and is_sender_counselor(message)
        and is_from_dm(message)
    ):
        sender: discord.User = message.author

        # checks if message was sent by the user and in the DM
        def check_same_user(client_response: discord.Message):
            sender_dm_id = sender.dm_channel.id
            return (
                client_response.author == sender
                and client_response.channel.id == sender_dm_id
            )

        await sender.send(content="Cual va a ser el nombre de la actividad?")
        activity_name = await client.wait_for("message", check=check_same_user)
        activity_name = activity_name.content

        await sender.send(content="Escribe el link del video para 'stream':")
        activity_url = await client.wait_for("message", check=check_same_user)
        activity_url = activity_url.content

        await client.change_presence(
            activity=discord.Activity(
                name=activity_name,
                url=activity_url,
                type=discord.ActivityType.streaming,
                state="Watching",
                details=f"Viewing {activity_name}",
            )
        )

        await client.wait_for("message", check=check_same_user)

        await client.change_presence(activity=None)


# This is a command method
async def join_voice_channel(client: discord.Client, message: discord.Message):
    if message.content == "!join":
        if not is_sender_counselor(message):
            log.info(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command"
                f" {message.content}"
            )
            await message.author.send(
                f"{message.author.nick}, no tienes los permisos para usar este comando"
            )
            return

        if not hasattr(message.author, "voice"):
            await message.author.send("No puedes unirme a un canal de voz desde el DM")
            return

        user_name = None

        if hasattr(message.author, "nick"):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_state: discord.VoiceState = message.author.voice
        log.info(f"[ Author Voice State] {voice_state}")
        if not voice_state:
            await message.author.send(
                f"Hola {user_name}, primero te tienes que conectar tu al canal de voz"
                " para yo saber a cual quieres que me conecte"
            )
            return

        voice_channel: discord.VoiceChannel = voice_state.channel

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild
        )

        # verify ownreship of music streaming
        if __MusicPlayerState.USER_PLAYING_MUSIC is None:
            # add ownership is no one has it
            __MusicPlayerState.USER_PLAYING_MUSIC = user_name
        elif __MusicPlayerState.USER_PLAYING_MUSIC != user_name:
            # no eres quien hizo el join original
            await message.author.send(
                f"Hola {user_name}, no tienes la autorización para unirme a el canal"
                f" **'{voice_channel}'**. **{__MusicPlayerState.USER_PLAYING_MUSIC}**"
                " tiene control del bot streamer."
            )
            return

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(voice_channel)
            print(f"The bot has moved to {voice_channel}")
        else:
            await voice_channel.connect()

        await message.author.send(f"Ya me uni al canal de voz: {voice_channel}")


# This is a command method
async def leave_voice_channel(client: discord.Client, message: discord.Message):
    if message.content == "!leave":
        if not is_sender_counselor(message):
            log.info(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command"
                f" {message.content}"
            )
            await message.author.send(
                f"{message.author.nick}, no tienes los permisos para usar este comando"
            )
            return

        if not hasattr(message.author, "voice"):
            await message.author.send("No me puedes sacar a un canal de voz desde el DM")
            return

        user_name = None

        if hasattr(message.author, "nick"):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_state: discord.VoiceState = message.author.voice
        log.info(f"[ Author Voice State] {voice_state}")
        if not voice_state:
            await message.author.send(
                f"Hola {user_name}, primero te tienes que conectar tu al canal de voz"
                "para yo saber de cual quieres que me desconecte"
            )
            return

        voice_channel: discord.VoiceChannel = voice_state.channel

        log.info(f"{client.voice_clients}")

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild
        )

        if not voice_client or voice_client.channel != voice_channel:
            await message.author.send(f"No estoy conectado al canal: {voice_channel}")
            return

        # verify ownreship of music streaming
        if __MusicPlayerState.USER_PLAYING_MUSIC != user_name:
            # no eres quien hizo el join original
            await message.author.send(
                f"Hola {user_name}, no tienes la autorización para removerme del canal"
                f" **'{voice_channel}'**. **{__MusicPlayerState.USER_PLAYING_MUSIC}**"
                " tiene control del bot streamer."
            )
            return
        else:
            # clean ownership of music streaming
            __MusicPlayerState.USER_PLAYING_MUSIC = None

        if voice_client.is_connected():
            await voice_client.disconnect()
            await message.author.send(
                f"Ya me desconecté del canal de voz: {voice_channel}"
            )


# This is a command method
async def play_audio(client: discord.Client, message: discord.Message):
    sections = message.content.split(" ")

    if sections[0] != "!play":
        return

    if __MusicPlayerState.PLAYING:
        if __MusicPlayerState.CURRENT_USER_PLAYING_MUSIC != message.author:
            return

    if not is_sender_counselor(message):
        log.info(
            f"[PREPA_BREACH] user {message.author.nick} tried to to command"
            f" {message.content}"
        )
        await message.author.send(
            f"{message.author.nick}, no tienes los permisos para usar este comando"
        )
        return

    if not hasattr(message.author, "voice"):
        await message.author.send("No puedes unirme a un canal de voz desde el DM")
        return

    user_name = None

    if hasattr(message.author, "nick"):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    if len(sections) < 2:
        await message.author.send(
            f"{user_name}, te falto el URL del video o cancion. Puede ser de cualquier"
            " website publico. (Youtube, Soundcloud, etc.)"
        )
        return

    url = sections[1]

    global _TMP_AUDIO_FILE

    try:
        if os.path.isfile(_TMP_AUDIO_FILE):
            os.remove(_TMP_AUDIO_FILE)
    except PermissionError:
        await message.author.send(
            "No puedo dar play a otra cancion. Un audio esta en play.\nPonlo en pausa."
        )
        return

    voice_client: discord.VoiceClient = discord.utils.get(
        client.voice_clients, guild=message.guild
    )

    if not voice_client:
        await message.author.send("No estoy conectado a ningún canal de voz")
        return

    if voice_client.is_playing():
        await message.author.send(
            "No puedo darle PLAY a un audio mientras uno esta en PLAY. Intenta pausar el"
            " audio primero"
        )
        return

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(paths.AUDIO, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

    except youtube_dl.DownloadError as err:
        log.error(f"{err}")
        await message.author.send(
            f"Me econtre con un error descargando el video.\nError:\n{str(err)}"
        )
        return

    name = ""
    for file in os.listdir(os.path.join(paths.AUDIO)):
        if file.endswith(".mp3"):
            name = file
            os.rename(os.path.join(paths.AUDIO, file), _TMP_AUDIO_FILE)

    voice_client.play(discord.FFmpegPCMAudio(_TMP_AUDIO_FILE))
    name = name.replace(".mp3", "").rsplit("-", 2)

    await message.author.send(f"{user_name}, ya **'{name} '** esta en PLAY")


# This is a command method
async def pause_audio(client: discord.Client, message: discord.Message):
    if message.content == "!pause":
        if not is_sender_counselor(message):
            log.info(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command"
                f" {message.content}"
            )
            await message.author.send(
                f"{message.author.nick}, no tienes los permisos para usar este comando"
            )
            return

        if not hasattr(message.author, "voice"):
            await message.author.send("No puedes pausar a un canal de voz desde el DM")
            return

        user_name = None

        if hasattr(message.author, "nick"):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild
        )

        if not voice_client:
            await message.author.send(
                f"{user_name}, No estoy conectado a ningún canal de voz"
            )
            return

        voice_channel: discord.VoiceChannel = voice_client.channel

        if voice_client.is_playing():
            voice_client.pause()
            await message.author.send(f"Pausado en el canal {voice_channel}")


# This is a command method
async def resume_audio(client: discord.Client, message: discord.Message):
    if message.content == "!resume":
        if not is_sender_counselor(message):
            log.info(
                f"[PREPA_BREACH] user {message.author.nick} tried to to command"
                f" {message.content}"
            )
            await message.author.send(
                f"{message.author.nick}, no tienes los permisos para usar este comando"
            )
            return

        if not hasattr(message.author, "voice"):
            await message.author.send("No puedes pausar a un canal de voz desde el DM")
            return

        user_name = None

        if hasattr(message.author, "nick"):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        voice_client: discord.VoiceClient = discord.utils.get(
            client.voice_clients, guild=message.guild
        )

        if not voice_client:
            await message.author.send(
                f"${user_name}, No estoy conectado a ningún canal de voz"
            )
            return

        voice_channel: discord.VoiceChannel = voice_client.channel

        if voice_client.is_paused():
            voice_client.resume()
            await message.author.send(f"Resumido en el canal {voice_channel}")


async def download_user_level_data(message: discord.Message):
    CMD = "!get-leaderboard"

    if message.content != CMD:
        return

    if not (is_sender_counselor(message) or is_sender_admin(message)):
        return  # sad face, not Estudiante Orientador or ADMIN

    # Send leveling data
    await message.author.send(
        content="Hola, aquí envió la data del **Leaderboard de Mensajes**",
        file=discord.File(LEVEL_PATH),
    )
