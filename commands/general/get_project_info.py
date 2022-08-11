"""
//  /bot-discord/commands/general/get_project_info.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/11
//  
//  Last Modified: Thursday, 11th August 2022 2:31:49 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import json
import os
from typing import Dict, Tuple

from constants import paths
from discord import Interaction, Embed
from discord.app_commands import Command, Choice


_PROJECT_EMBEDS = {}

_PROJECT_IDS: Tuple[Tuple[str, str]] = None

_PROJECT_DICT: Dict[str, Dict[str, str]] = None


"""
Why load the json data file once and store into a global variable?

Because opening a file multiple times is an expensive OS operation and we want the bot 
to be as smooth as possible. Looking for data already allocated in the process virtual 
memory is relatively inexpensive compared to opening a file multiple times.

Why save the embeds and not create then on each request?

Caching the embeds saves us CPU cycles in creating and allocating data for an object that is 
static and will never change as long as the app is running.
"""


def command():
    global _PROJECT_IDS, _PROJECT_DICT
    # Register Command

    project_info_path = os.path.join(paths.PROJECTS, "proyectos.json")

    # load file into memory once.
    with open(project_info_path, "r") as project_file:
        # import data from JSON as a Dict of Dicts
        _PROJECT_DICT = json.load(project_file)

        # for every project create a tuple with its FULL NAME and ID as value
        tmp = []
        for project_id, proj_info in _PROJECT_DICT.items():
            tmp.append(
                (
                    project_id,
                    f"{project_id.upper()} - {proj_info.get('title')}",
                )
            )
        # To use in the Autocomplete
        # Save as tuple, because it is immutable
        _PROJECT_IDS = tuple(tmp)

    # create Command instance
    command = Command(
        name="ls_projects",
        description="Provee información sobre proyectos e investigaciones relacionadas a INEL/ICOM/INSO/CIIC",
        callback=_prj_info,
    )

    # assign Autocomplete
    @command.autocomplete("project_id")
    async def project_autocomplete(_: Interaction, current: str):
        # python list comprehension
        # iterate through the _PROJ_IDS tuple of names and project_ids
        # if the current input is a substring of the Project Name
        # return as a Choice, with name and project_id as value
        return [
            Choice(name=name, value=project_id)
            for project_id, name in _PROJECT_IDS
            if current.lower() in name.lower()
        ]

    return command


async def _prj_info(interaction: Interaction, project_id: str):
    if project_id in _PROJECT_EMBEDS:
        return await interaction.response.send_message(
            embed=_PROJECT_EMBEDS[project_id]
        )

    abbreviations = ", ".join(map(lambda project: project[0], _PROJECT_IDS))

    if project_id is None:
        return await interaction.response.send_message(
            f"No me dijiste el nombre del proyecto que quieres buscar.\nIntenta con alguno de: {abbreviations}"
        )

    if _PROJECT_DICT.get(project_id) is None:
        return await interaction.response.send_message(
            f"No tenemos información de este proyecto.\nIntenta con alguno de: {abbreviations}"
        )

    embed: Embed = Embed.from_dict(_PROJECT_DICT[project_id])
    await interaction.response.send_message(
        content=f"Esta es la información del \"{_PROJECT_DICT[project_id].get('title', project_id)}\"\n",
        embed=embed,
    )
