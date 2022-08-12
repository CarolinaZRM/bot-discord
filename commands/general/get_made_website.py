"""
// /bot-discord/commands/general/_made_website.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/10
//  
//  Last Modified: Wednesday, 10th August 2022 7:34:22 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import os

import discord
from constants import paths
from discord.app_commands import Command

_MADE_WEBSITE = os.path.join(paths.IMAGES, "MadeWeb.png")


def command():
    return Command(
        name="made-web",
        description="Enlace a la página web de la consejera de INEL/ICOM/INSO/CIIC, Madeline Rodríguez",
        callback=_made_website,
    )


async def _made_website(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Aquí el enlace para la página web de Made! :green_heart: \n"
        "https://sites.google.com/upr.edu/maderodriguez/\n",
        file=discord.File(_MADE_WEBSITE),
    )
