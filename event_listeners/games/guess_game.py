"""
//  /bot-discord/listeners/games/guess_game.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/13
//
//  Last Modified: Saturday, 13th August 2022 11:52:48 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import random

from discord import Client, Message

import log


async def on_message(message: Message, client: Client):
    log.info("Entered guessing game")
    if message.content == "?guess":

        def convert_to_int(value):
            try:
                return int(value)
            except Exception:
                return False

        response = None
        user_name = None

        if hasattr(message.author, "nick"):
            user_name = message.author.nick
        else:
            user_name = message.author.name

        if user_name is None:
            user_name = message.author.name
        await message.channel.send(
            "Tengo un numero secreto del 1 al 100 :upside_down: ¿Puedes"
            " adivinarlo?\nHint: Es un numero entero :eyes:\nSi te rindes escribe"
            " 'MeRindo' y te diré el numero."
        )
        correct_answer = random.randint(1, 100)

        while convert_to_int(response) != correct_answer:
            response = await client.wait_for(
                "message",
                check=lambda response_message: response_message.author == message.author,
            )
            response = response.content

            if convert_to_int(response) is not False:
                if (convert_to_int(response) > 100) or (convert_to_int(response) <= 0):
                    await message.channel.send(
                        "Heyyy?? ESe numero no está entre 1 y 100 Jajajaja\nIntenta"
                        f" otra vez {user_name}! :sweat_smile::joy:"
                    )
                    continue
                elif convert_to_int(response) > correct_answer:
                    await message.channel.send(f"Más pequeño {user_name}!")
                    continue
                elif convert_to_int(response) < correct_answer:
                    await message.channel.send(f"Más grande {user_name}!")
                    continue
            elif response == "MeRindo":
                break

        if response != "MeRindo":
            await message.channel.send(f"Lo adivinaste {user_name}! Yey!")
        else:
            await message.channel.send(
                f"Te rendiste tan rápido {user_name}? El numero era {correct_answer}"
            )
