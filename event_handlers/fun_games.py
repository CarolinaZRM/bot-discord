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

import random
import log


async def event_ping_pong(message: str):
    if message.content.lower() == 'ping':
        await message.channel.send('Pong :)')


async def event_guessing_game(message, client):
    log.debug('[DEBUG] Entered guessing game')
    if message.content == "?guess":
        def convert_to_int(value):
            try:
                return int(value)
            except Exception as _:
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
        correct_answer = random.randint(1, 101)

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
