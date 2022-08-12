"""
//  /handlers/help_menu/counselor_menu.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/24/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

from . import base_menu


def help_menu_for_counselor():
    embed = base_menu.help_menu_base()
    embed.add_field(
        name="!user-count",
        value="Provee la cantidad de miembros en el canal/grupo actual.\n",
    )
    embed.add_field(
        name="!admin_add_profanity:PALABRA",
        value=(
            "Este comando solo para consejeros permite añadir una palabra nueva a la"
            " lista de profanidades. Utilice con cuidado."
        ),
    )
    embed.add_field(
        name="!botstartstream",
        value=(
            "Este comando es para hacer el *MADE Bot* se comporte como si estuviera"
            " 'Streaming' esto hara que aparezca un link en su perfil.Pregunta por"
            " nombre de la actividad y el URL del video. Tiene que ser un video publico."
            " Utilice con cuidado"
        ),
    )
    embed.add_field(
        name="!botstopstream",
        value=(
            'Este comando Hace que el bot termine de "stream" un video y vuelva a un'
            " estado normal. Utilice con cuidado."
        ),
    )
    return embed
