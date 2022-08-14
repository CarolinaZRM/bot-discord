"""
//  /handlers/telephone_guide/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
from discord.app_commands import CommandTree, Group

import log

from . import (
    asesoria_academica,
    asistencia_econ,
    decanato_estudiantes,
    dept_cons_psicologicos,
    dept_contact,
    faculty,
    guardia_universitaria,
    list_help,
)


async def subscribe_commands(command_tree: CommandTree = None):
    log.info("subscribing Telephone Guide...")
    grp = Group(
        name="telephone_guide", description="Información de Contactos disponibles"
    )
    modules = (
        asesoria_academica,
        asistencia_econ,
        decanato_estudiantes,
        dept_cons_psicologicos,
        dept_contact,
        faculty,
        guardia_universitaria,
    )

    try:
        help_list = []
        for module in modules:
            if hasattr(module, "command"):
                grp.add_command(module.command())
            else:
                raise Exception(f"The module {module} does not have command() function")

            if hasattr(module, "help_data"):
                help_list.append(module.help_data())
            else:
                raise Exception(
                    f"The module {module} does not have help_data() function"
                )

        grp.add_command(list_help.command(help_list))
    except Exception as e:
        log.error(f"{e}")

    try:
        command_tree.add_command(grp)
    except Exception as e:
        log.error(f"{e}")

    log.info("Finished subscribing...")


__all__ = [
    subscribe_commands,
]
