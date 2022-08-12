import os
import log


from discord import Interaction, Embed
from discord.app_commands import Command

from constants import paths

_RULE_FILE = os.path.join(paths.TEXT_FILES, "rules.txt")

_RULES_EMBED = None


def __init_rules():
    global _RULES_EMBED
    _RULES_EMBED = Embed(
        title="Reglas del Servidor de Discord Oficial de Team MADE",
        description="Aquí están todas las reglas a seguir en el servidor en esta semana de orientación virtual 2022",
    )

    rules = open(_RULE_FILE, "r")

    ruleCount = 1

    for rule in rules:
        _RULES_EMBED.add_field(name=f"""Regla {ruleCount}""", value=rule)
        ruleCount += 1


def command():
    __init_rules()

    return Command(
        name="reglas", description="Reglas del Servidor", callback=_server_rules
    )


async def _server_rules(interaction: Interaction):
    log.info("[RULE-DBG] Entered Rule Generator")

    if not _RULES_EMBED:
        __init_rules()

    await interaction.response.send_message(content=None, embed=_RULES_EMBED)
