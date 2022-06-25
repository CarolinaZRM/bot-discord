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
import json
import os
import time

import discord
import youtube_dl
from discord.channel import ChannelType
from discord.errors import Forbidden

import config
import log
from constants import admins, paths

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

    guild: discord.Guild = client.get_guild(config.GUILD_ID_NUM)

    for member in guild.members:
        for role in member.roles:
            if role.name == "EstudianteOrientador" \
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
            if role.name == 'EstudianteOrientador' \
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


# This is a command method
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


# This is a command method
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


# This is a command method
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


# This is a command method
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


# This is a command method
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


# This is a command method
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


# Leveling System Methods
LEVEL_PATH = os.path.join(paths.ROOT_PATH, "users.json")

if not os.path.exists(LEVEL_PATH):
    with open(LEVEL_PATH, 'w') as file:
        file.write('{}')

# Runs when a member joins the server, adds user to the json with level 1


async def level_join(member):
    with open(LEVEL_PATH, 'r') as levels_file:
        users = json.load(levels_file)

    await update_data(users, member)

    with open(LEVEL_PATH, 'w') as levels_file:
        json.dump(users, levels_file, indent=True)


# Runs on message, the user is given a certain amount of experience for each message and we check for level up
async def level_on_message(message: discord.Message):
    if not message.author.bot:
        with open(LEVEL_PATH, 'r') as levels_file:
            users = json.load(levels_file)

        messageLength = int(len(message.content))

        # give a max Experience of 5
        exp = min(messageLength, 5)

        await update_data(users, message.author)
        await add_experience(users, message.author, exp)
        await level_up(users, message.author, message.channel)

        # Updates the nickname for the given user
        users[f'{message.author.id}']['nickname'] = message.author.display_name

        users[f'{message.author.id}']['messages'] += 1

        with open(LEVEL_PATH, 'w') as levels_file:
            json.dump(users, levels_file, indent=True)

# If not already in the file add the user to the json file with experience 0 and level 1


async def update_data(users, user):
    if f'{user.id}' not in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['nickname'] = getattr(user, 'nick', user.name)
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['messages'] = 0


# Add a variable number of exp to the json file for a user
async def add_experience(users, user, exp):
    BUFFER = 15  # seconds
    current_time = int(time.time())

    if 'timestamp' in users[f'{user.id}']:
        if current_time < BUFFER + users[f'{user.id}']['timestamp']:
            # return if buffer has not been completed
            return

    users[f'{user.id}']['timestamp'] = int(time.time())

    users[f'{user.id}']['experience'] += exp


# Check for level up condition given by lvl_end also send a message on level up
async def level_up(users, user, channel):
    experience = users[f'{user.id}']["experience"]
    lvl_start = users[f'{user.id}']["level"]
    lvl_end = int(experience / (100 + ((lvl_start - 1) * 15)))

    if lvl_start < lvl_end:
        await channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']["level"] = lvl_end


async def general_leaderboard(message: discord.Message):
    CMD = '!leaderboard'

    if message.content.lower() != CMD:
        return

    with open(LEVEL_PATH, 'r') as top10:
        leaderboard_data = json.load(top10)

    top_peeps = [user_id for user_id, _ in sorted(
        leaderboard_data.items(),
        key=lambda item: int(item[1]['experience']), reverse=True)[0:10]
    ]

    top_crewmates = []

    for position, user_id in enumerate(top_peeps):
        # add 1 to position to make the index start from 1
        top_crewmates.append(
            f"{position + 1} - <@!{user_id}>\t|\tLevel: {leaderboard_data[user_id]['level']}")

    embed = discord.Embed(
        title=":trophy: Leaderboard :trophy:", color=11901259)

    embed.add_field(name="Crewmates", value='\n'.join(
        top_crewmates), inline=False)

    await message.channel.send(embed=embed)


LEVEL_ICONS = {
    1: "https://cdn.discordapp.com/attachments/856635443310362624/870329147120058399/image0.png",
    2: "https://cdn.discordapp.com/attachments/856635443310362624/870329147531079700/image1.png",
    3: "https://cdn.discordapp.com/attachments/856635443310362624/870329147795316796/image2.png",
    4: "https://cdn.discordapp.com/attachments/856635443310362624/870329148437069956/image3.png",
    5: "https://cdn.discordapp.com/attachments/856635443310362624/870329148730650624/image4.png",
    6: "https://cdn.discordapp.com/attachments/856635443310362624/870329148982296656/image5.png",
    7: "https://cdn.discordapp.com/attachments/856635443310362624/870329149548556288/image7.jpg",
    8: "https://cdn.discordapp.com/attachments/856635443310362624/870329149917659146/image8.png",
    9: "https://cdn.discordapp.com/attachments/856635443310362624/870329150219640892/image9.jpg",
    10: "https://cdn.discordapp.com/attachments/856635443310362624/870329146461552701/image1.jpg",
}


async def leveling_status(message: discord.Message):
    # With command "!level"
    if not message.author.bot and message.content.lower() == "!level":
        with open(LEVEL_PATH, 'r') as levels_file:
            users = json.load(levels_file)

        user = message.author

        user_level = users[f'{user.id}']["level"]

        imageurl = LEVEL_ICONS.get(user_level) or LEVEL_ICONS.get(10)

        embed = discord.Embed(title=f'Character Status: {getattr(user, "nick", user.name)}',
                              description="Status of you character in the Team Made Leveling System", color=0x4dab03)
        embed.add_field(
            name="Level", value=users[f'{user.id}']['level'], inline=True)
        embed.add_field(name="Experience",
                        value=users[f'{user.id}']['experience'], inline=True)
        embed.add_field(name="Number of Messages",
                        value=users[f'{user.id}']['messages'], inline=True)
        embed.set_image(url=imageurl)

        await message.channel.send(embed=embed)


async def download_user_level_data(message: discord.Message):
    CMD = '!get-leaderboard'

    if message.content != CMD:
        return

    if not (is_sender_counselor(message) or is_sender_admin(message)):
        return  # sad face, not Estudiante Orientador or ADMIN

    # Send leveling data
    await message.author.send(content='Hola, aquí envió la data del **Leaderboard de Mensajes**', file=discord.File(LEVEL_PATH))


# Leveling System Methods
LEVEL_PATH = os.path.join(paths.ROOT_PATH, "users.json")

if not os.path.exists(LEVEL_PATH):
    with open(LEVEL_PATH, 'w') as file:
        file.write('{}')

# Runs when a member joins the server, adds user to the json with level 1


async def level_join(member):
    with open(LEVEL_PATH, 'r') as levels_file:
        users = json.load(levels_file)

    await update_data(users, member)

    with open(LEVEL_PATH, 'w') as levels_file:
        json.dump(users, levels_file, indent=True)


# Runs on message, the user is given a certain amount of experience for each message and we check for level up
async def level_on_message(message: discord.Message):
    if not message.author.bot:
        with open(LEVEL_PATH, 'r') as levels_file:
            users = json.load(levels_file)

        messageLength = int(len(message.content))

        # give a max Experience of 5
        exp = min(messageLength, 5)

        await update_data(users, message.author)
        await add_experience(users, message.author, exp)
        await level_up(users, message.author, message.channel)

        # Updates the nickname for the given user
        users[f'{message.author.id}']['nickname'] = message.author.display_name

        users[f'{message.author.id}']['messages'] += 1

        with open(LEVEL_PATH, 'w') as levels_file:
            json.dump(users, levels_file, indent=True)

# If not already in the file add the user to the json file with experience 0 and level 1


async def update_data(users, user):
    if f'{user.id}' not in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['nickname'] = getattr(user, 'nick', user.name)
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['messages'] = 0


# Add a variable number of exp to the json file for a user
async def add_experience(users, user, exp):
    BUFFER = 15  # seconds
    current_time = int(time.time())

    if 'timestamp' in users[f'{user.id}']:
        if current_time < BUFFER + users[f'{user.id}']['timestamp']:
            # return if buffer has not been completed
            return

    users[f'{user.id}']['timestamp'] = int(time.time())

    users[f'{user.id}']['experience'] += exp


# Check for level up condition given by lvl_end also send a message on level up
async def level_up(users, user, channel):
    experience = users[f'{user.id}']["experience"]
    lvl_start = users[f'{user.id}']["level"]
    lvl_end = int(experience / (100 + ((lvl_start - 1) * 15)))

    if lvl_start < lvl_end:
        await channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']["level"] = lvl_end


async def general_leaderboard(message: discord.Message):
    CMD = '!leaderboard'

    if message.content.lower() != CMD:
        return

    with open(LEVEL_PATH, 'r') as top10:
        leaderboard_data = json.load(top10)

    top_peeps = [user_id for user_id, _ in sorted(
        leaderboard_data.items(),
        key=lambda item: int(item[1]['experience']), reverse=True)[0:10]
    ]

    top_crewmates = []

    for position, user_id in enumerate(top_peeps):
        # add 1 to position to make the index start from 1
        top_crewmates.append(
            f"{position + 1} - <@!{user_id}>\t|\tLevel: {leaderboard_data[user_id]['level']}")

    embed = discord.Embed(
        title=":trophy: Leaderboard :trophy:", color=11901259)

    embed.add_field(name="Crewmates", value='\n'.join(
        top_crewmates), inline=False)

    await message.channel.send(embed=embed)


LEVEL_ICONS = {
    1: "https://cdn.discordapp.com/attachments/856635443310362624/870329147120058399/image0.png",
    2: "https://cdn.discordapp.com/attachments/856635443310362624/870329147531079700/image1.png",
    3: "https://cdn.discordapp.com/attachments/856635443310362624/870329147795316796/image2.png",
    4: "https://cdn.discordapp.com/attachments/856635443310362624/870329148437069956/image3.png",
    5: "https://cdn.discordapp.com/attachments/856635443310362624/870329148730650624/image4.png",
    6: "https://cdn.discordapp.com/attachments/856635443310362624/870329148982296656/image5.png",
    7: "https://cdn.discordapp.com/attachments/856635443310362624/870329149548556288/image7.jpg",
    8: "https://cdn.discordapp.com/attachments/856635443310362624/870329149917659146/image8.png",
    9: "https://cdn.discordapp.com/attachments/856635443310362624/870329150219640892/image9.jpg",
    10: "https://cdn.discordapp.com/attachments/856635443310362624/870329146461552701/image1.jpg",
}


async def leveling_status(message: discord.Message):
    # With command "!level"
    if not message.author.bot and message.content.lower() == "!level":
        with open(LEVEL_PATH, 'r') as levels_file:
            users = json.load(levels_file)

        user = message.author

        user_level = users[f'{user.id}']["level"]

        imageurl = LEVEL_ICONS.get(user_level) or LEVEL_ICONS.get(10)

        embed = discord.Embed(title=f'Character Status: {getattr(user, "nick", user.name)}',
                              description="Status of you character in the Team Made Leveling System", color=0x4dab03)
        embed.add_field(
            name="Level", value=users[f'{user.id}']['level'], inline=True)
        embed.add_field(name="Experience",
                        value=users[f'{user.id}']['experience'], inline=True)
        embed.add_field(name="Number of Messages",
                        value=users[f'{user.id}']['messages'], inline=True)
        embed.set_image(url=imageurl)

        await message.channel.send(embed=embed)


async def download_user_level_data(message: discord.Message):
    CMD = '!get-leaderboard'

    if message.content != CMD:
        return

    if not (is_sender_counselor(message) or is_sender_admin(message)):
        return  # sad face, not Estudiante Orientador or ADMIN

    # Send leveling data
    await message.author.send(content='Hola, aquí envió la data del **Leaderboard de Mensajes**', file=discord.File(LEVEL_PATH))
