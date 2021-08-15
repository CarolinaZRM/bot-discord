"""
//
//  fun_games.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
import discord
import log
import random
import re


# This is a command method
async def event_ping_pong(message: str):
    if message.content.lower() == 'ping':
        await message.channel.send('Pong :)')


# This is a command method
async def event_guessing_game(message, client):
    log.debug('[DEBUG] Entered guessing game')
    if message.content == "?guess":
        def convert_to_int(value):
            try:
                return int(value)
            except Exception:
                return False

        response = None
        user_name = None

        if hasattr(message.author, 'nick'):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        if user_name is None:
            user_name = message.author.name
        await message.channel.send("Tengo un numero secreto del 1 al 100 :upside_down: ¿Puedes adivinarlo?\nHint: Es un numero entero :eyes:\n"
                                   "Si te rindes escribe 'MeRindo' y te diré el numero.")
        correct_answer = random.randint(1, 100)

        while convert_to_int(response) != correct_answer:
            response = await client.wait_for("message", check=lambda response_message: response_message.author == message.author)
            response = response.content

            print('wut ?')
            print(response)
            print(f'Conver to int: {convert_to_int(response)}')

            if convert_to_int(response) is not False:
                if (convert_to_int(response) > 100) or (convert_to_int(response) <= 0):
                    await message.channel.send(f"""Heyyy?? ESe numero no está entre 1 y 100 Jajajaja\nIntenta otra vez {user_name}! :sweat_smile::joy:""")
                    continue
                elif convert_to_int(response) > correct_answer:
                    await message.channel.send(f"""Más pequeño {user_name}!""")
                    continue
                elif convert_to_int(response) < correct_answer:
                    await message.channel.send(f"""Más grande {user_name}!""")
                    continue
            elif response == "MeRindo":
                break

        if response != "MeRindo":
            await message.channel.send(f"""Lo adivinaste {user_name}! Yey!""")
        else:
            await message.channel.send(f"""Te rendiste tan rapido {user_name}? El numero era {correct_answer}""")


def make_bold(string: str):
    return f'**{string}**'


async def event_rock_paper_scissor(message: discord.Message, client: discord.Client):
    CMD = '!rps'

    user_name = getattr(message.author, 'nick', message.author.name)

    if re.fullmatch(CMD, message.content):
        await message.channel.send(f'Wepa _{user_name}_! Vamos a jugar Rock-Paper-Scissors :grimacing:\nYa hice mi movida, ahora haz la tuya :wink:')
        # play against bot
        PLAYS = ['scissors', 'paper', 'rock']

        # select random play for bot
        bot_play: str = random.choice(PLAYS)

        while True:
            user_answer = await client.wait_for("message", check=lambda response_message: response_message.author == message.author)
            user_answer = user_answer.content.lower()

            if user_answer not in PLAYS:
                bolded_plays = map(make_bold, PLAYS)
                await message.channel.send(f'Whoops... **Esa jugada no es valida** {user_name}\nPuedes jugar una de: {", ".join(bolded_plays)}')
            else:
                break

        if bot_play == user_answer:
            await message.channel.send('Empate :tada:')
        elif (PLAYS.index(user_answer) + 1) % 3 == PLAYS.index(bot_play):
            await message.channel.send(f'AHH jugué {bot_play.upper()} :worried: ...\nPues Ganaste _{user_name}_, Congrats! :fire: :100:')
        else:
            await message.channel.send(f'Uff, Perdiste _{user_name}_ :pleading_face:\nYo había jugado {bot_play.upper()} :grimacing:')
