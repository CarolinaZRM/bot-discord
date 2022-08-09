'''
//  /handlers/help_menu/base_menu.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/24/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
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
    # embed.add_field(
    #     name="!emails", value="Gives user a PDF with some important emails they can use")
    embed.add_field(
        name="!salon:SALON", value="Provee información sobre el edificio donde se puede encontrar ese salón.\n"
        "Ejemplo: *!salon:S123*.\tSi el salón comienza con una letra entonces debe dividir la letra que identifica al edificio y el numero del salón con un guión (-).\n"
        "Ejemplo: *!salon:F-B*, este es el Anfiteatro B del edificio de Física"
    )
    embed.add_field(
        name='!calendario',
        value="Provee un enlace rapido al Calendario Académico de UPRM."
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
        value='Provee información de la guardia universitaria, policía estatal y otros servicios de emergencia regionales.'
    )
    embed.add_field(
        name='!eo:DEPT',
        value="Provee una lista los usernames (@'s) de los Estudiantes Orientadores de ese DEPT. Puedes escoger entre: INEL, ICOM, INSO o CIIC."
    )
    embed.add_field(
        name="!ls_student_orgs:ORG",
        value="Provee información sobre organizaciones estudiantiles relacionadas a INEL/ICOM/INSO/CIIC\n"
        "(IEEE/EMC/HKN/RAS_CSS/COMP_SOC/CAS/PES/WIE/ACM_CSE/CAHSI/SHPE/ALPHA_AST/EMB/PHOTONICS)"
    )
    embed.add_field(
        name="!ls_projects:PROJECT",
        value="Provee información sobre proyectos e investigaciones relacionadas a INEL/ICOM/INSO/CIIC"
    )
    return embed
