"""
//
//  help_menu.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""

import discord
import log


def help_menu_base():
    log.debug('[DEBUG] Enter Counselor Help')
    embed = discord.Embed(title="Lista de Commandos")

    embed.add_field(name="!help",
                    value="Mostrara la lista de los commandos disponibles.")
    embed.add_field(name="!curriculo:DEPT",
                    value="Te proveéra un PDF del curriculo del DEPT (INEL/ICOM/INSO/CIIC)")
    embed.add_field(
        name="!map", value="Provee un enlace a el Mapa de UPRM")
    embed.add_field(
        name="!links", value="Gives the user a PDF with all the important links of UPRM")
    embed.add_field(
        name="!emails", value="Gives user a PDF with some important emails they can use")
    embed.add_field(
        name="!salon:SALON", value="Provee información sobre el edificio donde se puede encontrar ese salón.\n"
        "Ejemplo: *!salon:S123*.\tSi el salón comienza con una letra entonces debe dividir la letra que identifica al edificio y el numero del salón con un guión (-).\n"
        "Ejemplo: *!salon:F-B*, este es el Anfiteatro B del edificio de Física"
    )
    embed.add_field(
        name='!calendario',
        value="Provee un enlace rapido al Calendario Academico de UPRM."
    )
    embed.add_field(
        name='!contactos',
        value='Mostrara una lista de todos los contactos que tengo disponible para ofrecerte.'
    )
    embed.add_field(
        name="!dept:DEPT", value="Provee información sobre el DEPT (INEL/ICOM or INSO/CIIC).\n"
        "Localización de la oficina, horas de trabajo, numero de teléfono, extensión, etc."
    )
    embed.add_field(
        name="!facultad:DEPT",
        value="Provee información de contacto para facultad del DEPT (INEL/ICOM/INSO/CIIC).\n"
    )
    embed.add_field(
        name='!guardia',
        value='Provee informacion de la guardia universitaria, policia estatal y otros servicios de emergencia regionales.'
    )
    embed.add_field(
        name='/eo:DEPT',
        value="Provee una lista los usernames (@'s) de los Estudiantes Orientadores de ese DEPT. Puedes escoger entre: INEL, ICOM, INSO o CIIC."
    )
    return embed


def help_menu_for_prepa():
    return help_menu_base()


def help_menu_for_counselor():
    embed = help_menu_base()
    embed.add_field(
        name="!user-count",
        value="Provee la cantidad de mienbros en el canal/grupo actual.\n"
    )
    embed.add_field(
        name='!admin_add_profanity:PALABRA',
        value='Este comando solo para consejeros permite anadir una palabra nueva a la lista de profanidades. Utilice con cuidado.'
    )
    embed.add_field(
        name='!botstartstream',
        value="Este comando es para hacer el *MADE Bot* se comporte como si estuviera 'Streaming' esto hara que aparezca un link en su perfil."
        "Pregunta por nombre de la actividad y el URL del video. Tiene que ser un video publico. Utilice con cuidado"
    )
    embed.add_field(
        name='!botstopstream',
        value='Este comando Hace que el bot termine de "stream" un video y vuelva a un estado normal. Utilice con cuidado.'
    )
    return embed


def help_menu_join():
    return help_menu_base()
