import csv
import os

import discord
from discord.app_commands import Command

from constants import paths

_FAQ_FILE = os.path.join(paths.TEXT_FILES, "faq.csv")


def command():
    return Command(
        name="faq",
        description="Frequently Asked Questions por Prepas",
        callback=_generate_faq,
    )


__FAQ_EMBED = None


def __init_faq_embed():
    global __FAQ_EMBED

    __FAQ_EMBED = discord.Embed(
        title="Frequently Asked Questions",
        description=(
            "Aquí puedes encontrar ciertas preguntas que pueden surgir durante la semana"
        ),
    )

    with open(_FAQ_FILE) as faq_file:
        rows = csv.DictReader(faq_file, delimiter=";")
        for row in rows:
            question = dict(row)
            __FAQ_EMBED.add_field(
                name=f"{question['num']}) {question['question']}",
                value=question["answer"],
            )


async def _generate_faq(interaction: discord.Interaction):
    if not __FAQ_EMBED:
        __init_faq_embed()

    await interaction.response.send_message(content=None, embed=__FAQ_EMBED)
