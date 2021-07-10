'''
//  /handlers/telephone_guide/telephone_guide_help.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import discord

from .asistencia_econ import get_asistencia_econ
from .consejeria_academica import get_consejeria_academica
from .decanato_estudiantes import get_decanato_estudiante
from .dept_cons_psicologicos import get_dept_cons_psicologicos
from .dept_info import get_dept_info
from .faculty import get_faculty
from .guardia_universitaria import get_guardia_universitaria


def get_telephone_guide_help(sections):
    embed = discord.Embed(title='Lista de Contactos disponibles')
    embed.add_field(
        name='Uso',
        value='!<CONTACTO> | Esto mostrara información revelante para el CONTACTO.'
    )

    for contact_name in _TELEPHONE_GUIDE_LIST:
        if _TELEPHONE_GUIDE_LIST[contact_name]['func'] and contact_name != '!contactos':
            cn_ts = contact_name
            if contact_name.lower() in ('!dept', '!facultad', '!consejeroacad'):
                cn_ts = f'{contact_name}:DEPT'
            embed.add_field(
                name=cn_ts,
                value=_TELEPHONE_GUIDE_LIST[contact_name]['description']
            )
    return embed


_TELEPHONE_GUIDE_LIST = dict(
    {
        '!aecon': {'func': get_asistencia_econ, 'description': 'Información de Contacto de Asistencia Económica'},
        '!consejeroacad': {'func': get_consejeria_academica, 'description': 'Obtener Información de Asesoría Académica y Consejería Profesional de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!contactos': {'func': get_telephone_guide_help, 'description': 'Obtener lista completa de contactos disponibles'},
        '!dcsp': {'func': get_dept_cons_psicologicos, 'description': 'Información del Departamento de Consejería y Servicios Psicológicos (DCSP)'},
        '!dec_estudiantes': {'func': get_decanato_estudiante, 'description': 'Obtener infomacion del Decanato de Estudiantes'},
        '!dept': {'func': get_dept_info, 'description': 'Obtener Información de contacto de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!facultad': {'func': get_faculty, 'description': 'Obtener información de contacto de la facultad de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!guardia': {'func': get_guardia_universitaria, 'description': 'Información de la guardia universitaria'},
        '!rectoria': {'func': None, 'description': 'Información de Contacto de Rectoria'},
        '!univa': {'func': None, 'description': 'Información sobre Univ Avanzado'},
    }
)


def is_command(sections):
    return len(sections) > 0 and sections[0] in _TELEPHONE_GUIDE_LIST


def get_guide_handler(sections):
    sect = sections[0].lower()
    return _TELEPHONE_GUIDE_LIST.get(sect)['func']
