import json
from typing import List

import log
from constants import paths
from discord import Embed, Interaction
from discord.app_commands import Choice, Command

_ORGANIZATIONS = [
    "IEEE",
    "EMC",
    "HKN",
    "RAS_CSS",
    "COMP_SOC",
    "CAS",
    "PES",
    "WIE",
    "ACM_CSE",
    "CAHSI",
    "SHPE",
    "ALPHA_AST",
    "EMB",
    "PHOTONICS",
]

_ORG_AVG = "/".join(_ORGANIZATIONS)

__ORG_EMBEDS = {}


def command():
    org_info_cmd = Command(
        name="ls_student_orgs",
        description="Provee información sobre organizaciones estudiantiles relacionadas a INEL/ICOM/INSO/CIIC",
        callback=_organization_info,
    )

    @org_info_cmd.autocomplete("student_org")
    async def orgs_autocomplete(
        interaction: Interaction,
        current: str,
    ) -> List[Choice[str]]:
        return [
            Choice(name=org, value=org)
            for org in _ORGANIZATIONS
            if current.lower() in org.lower()
        ]

    return org_info_cmd


async def _organization_info(interaction: Interaction, student_org: str):
    log.info("Entered Student Org")

    if student_org not in _ORGANIZATIONS:
        await interaction.response.send_message(
            "Puede que te hayas confundido :sweat_smile:\n"
            "'Org' = Organización\n"
            "Intenta usar el comando ```ls_student_orgs <org_name>``` sustituyendo <org_name> con una de las siguientes abreviaciones:\n"
            + _ORG_AVG
        )
        return

    if student_org in __ORG_EMBEDS:
        return await interaction.response.send_message(embed=__ORG_EMBEDS[student_org])

    with open(f"{paths.RESOURCES}/OrgInfo.json", "r") as orgInfo:
        orgInfoDict = json.load(orgInfo)
        orgDictObj = orgInfoDict.get(student_org.upper())

        if orgDictObj is None:
            return await interaction.response.send_message(
                "Organización no existe en lista, intenta usar una de las siguientes abreviaciones:\n"
                + _ORG_AVG
            )

        embed: Embed = Embed.from_dict(orgDictObj)
        __ORG_EMBEDS[student_org] = embed
        await interaction.response.send_message(embed=embed)
