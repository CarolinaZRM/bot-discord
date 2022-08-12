import os
from typing import Union

from discord import File, Interaction, Member, User
from discord.app_commands import Command

import log
from constants import paths

_GOOGLE_ADD_CALENDAR = os.path.join(paths.IMAGES, "google_add_calendar.png")


def command():
    log.info("CALENDAR MAP SUB")
    return Command(
        name="calendario",
        description="Provee un enlace rápido al Calendario Académico de UPRM.",
        callback=_get_calendar,
    )


async def _get_calendar(interaction: Interaction):
    log.info("Entering calendario...")

    author: Union[Member, User] = interaction.user
    user_name = None

    if hasattr(author, "nick"):
        user_name = author.nick
    else:
        user_name = author.name

    await interaction.response.send_message(
        f"Hola {user_name}! Aquí adjunto el calendario académico de UPRM.\n"
        "**Calendario Académico:** https://www.uprm.edu/decestu/calendario/\n\n"
        "También puedes añadir este calendario a tu calendario personal.\n"
        "Presta atención a la esquina inferior derecha del calendario.\nSe ve asi:",
        file=File(_GOOGLE_ADD_CALENDAR),
    )
