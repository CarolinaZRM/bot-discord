"""
//  /bot-discord/listeners/games/rock_paper_scissors.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/13
//
//  Last Modified: Saturday, 13th August 2022 11:53:08 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import random
import re
from typing import Union

from discord import Client, Member, Message, User


def make_bold(string: str):
    return f"**{string}**"


def check_same_user(author: Union[Member, User]):
    def _check_equal(message: Message):
        return message.author == author

    return _check_equal


CMD = "?rps"

# play against bot
BOT_PLAYS = ["piedra", "papel", "tijera"]

PLAYS = {
    "piedra": "piedra",
    "rock": "piedra",
    "papel": "papel",
    "paper": "papel",
    "tijera": "tijera",
    "scissors": "tijera",
}

HELP_ = ["piedra/rock", "papel/paper", "tijera/scissors"]

MOVE_WINS_TO = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}


async def on_message(message: Message, client: Client):
    user_name: str = message.author.display_name

    if re.fullmatch(CMD, message.content):
        await message.channel.send(
            f"Wepa _{user_name}_! Vamos a jugar Rock-Paper-Scissors :grimacing:\nYa hice"
            " mi movida, ahora haz la tuya :wink:"
        )

        # select random play for bot
        bot_play: str = random.choice(BOT_PLAYS)

        while True:
            user_answer: Message = await client.wait_for(
                "message", check=check_same_user(message.author)
            )
            user_answer = user_answer.content.lower()

            if user_answer not in PLAYS:
                await message.channel.send(
                    f"Whoops... **Esa jugada no es valida** {user_name}\nPuedes jugar"
                    f' una de: {", ".join(map(make_bold, HELP_))}'
                )
            else:
                break

        user_play = PLAYS[user_answer]

        if bot_play == user_play:
            await message.channel.send("Empate :tada:")
        elif MOVE_WINS_TO.get(user_play) == bot_play:
            await message.channel.send(
                f"AHH jugué {bot_play.upper()} :worried: ...\nPues Ganaste"
                f" _{user_name}_, Congrats! :fire: :100:"
            )
        else:
            await message.channel.send(
                f"Uff, Perdiste _{user_name}_ :pleading_face:\nYo había jugado"
                f" {bot_play.upper()} :grimacing:"
            )
