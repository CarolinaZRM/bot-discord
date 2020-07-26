"""
//
//  telephone_guide.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""

import discord
from handlers.contacts import departamentos, servicios, consejeria_profesional


def generate_embed(contact, embed):
    embed.add_field(name="Nombre del Dept.", value=contact.contact_name)
    embed.add_field(name="Descripción",
                    value=contact.contact_description)
    embed.add_field(name="Servicios Provistos",
                    value=contact.services_provided)
    embed.add_field(name="Oficina", value=contact.office_number)

    divisor = '\n\u2022 '
    phone_list = f"\u2022 {divisor.join(contact.phone_number)}"
    embed.add_field(name="Teléfono(s)", value=phone_list)

    if contact.extensions:
        extension_list = f"\u2022 {divisor.join(contact.extensions)}"
        embed.add_field(name="Extensión(es)", value=extension_list)

    embed.add_field(name="Horas de Trabajo", value=contact.work_hours)
    embed.add_field(name="Localización en Google Maps",
                    value=contact.gmaps_location)

    return embed


def get_dept_info(sections):

    if len(sections) <= 1:
        return 'Por favor, especifica abreviacion del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!dept:inso"'

    department_name: str = sections[1].lower()

    embed = None
    if department_name in ('inso', 'ciic'):
        cse = departamentos.CSEDepartment()
        embed = discord.Embed(title="Información del departamento de CSE",
                              description="Información Utíl de CSE")

        return generate_embed(cse, embed)

    elif department_name in ('icom', 'inel'):
        ece = departamentos.ECEDepartment()
        embed = discord.Embed(title="Información del departamento de ECE",
                              description="Información Utíl de ECE")
        return generate_embed(ece, embed)

    else:
        embed = "No reconozco ese departamento :eyes: :confused:\n"\
            "Intenta con: INEL, ICOM, INSO o CIIC"

    return embed


def get_asistencia_econ(section):
    asis_econ = servicios.AsistenciaEconomica()

    return_message = "Esta es la informacion de la Oficina de Asistencia Economica:\n\n"

    embed = discord.Embed(title='Info Asistencia Economica',
                          description='Informacion Rapida')

    generate_embed(asis_econ, embed)
    embed = embed.add_field(name='Fechas Importantes (Prestamos, Beca, etc.)',
                            value=asis_econ.important_dates_link, inline=True)

    return {
        'embed': embed,
        'content_first': return_message
    }


def get_guardia_universitaria(section):
    guardia = servicios.GuardiaUniversitaria()
    embed = discord.Embed(title='Info Guardia Universitaria',
                          description='Informacion Rapida')
    ember = generate_embed(guardia, embed)

    divisor = '\n\u2022 '
    additional_info_list = f"\u2022 {divisor.join(guardia.additional_helpful_info)}"
    embed.add_field(name="Más Información Utíl", value=additional_info_list)
    embed.add_field(name="Enlaces Utíles", value=guardia.more_info_link)

    return embed


def get_telephone_guide_help(sections):
    embed = discord.Embed(title='Lista de Contactos disponibles')
    embed.add_field(
        name='Uso',
        value='!<CONTACTO> | Esto mostrara informacion revelante para el CONTACTO.'
    )

    for contact_name in _telephone_guide_list:
        if _telephone_guide_list[contact_name]['func'] and contact_name != '!contactos':
            cn_ts = contact_name
            if contact_name.lower() in ('!dept', '!facultad', '!consejeroacad'):
                cn_ts = f'{contact_name}:DEPT'
            embed.add_field(
                name=cn_ts,
                value=_telephone_guide_list[contact_name]['description']
            )
    return embed


def get_faculty(sections):
    cse_faculty = {
        "Bienvenido Velez Rivera": "Acting Dean of Engineering\nFull Time Professor\nbienvenido.velez@upr.edu",
        "Pedro I. Rivera Vega": "Acting CSE Director\nFull Time Professor\np.rivera@upr.edu",
        "Manuel Rodriguez Martinez": "Associate Director\nFull Time Professor\nmanuel.rodriguez7@upr.edu",
        "Wilson Rivera Gallego": "Full Time Professor\nwilson.riveragallego@upr.edu",
        "Kejie Lu": "Full Time Professor\nkejie.lu@upr.edu",
        "Heidy Sierra Gil": "Associate Professor\nheidy.sierra1@upr.edu",
        "Emmanuel Arzuaga Cruz": "Full Time Professor\nearzuaga@ece.uprm.edu",
        "Marko Schütz Schmuck": "Full Time Professor\nmarko.schutz@upr.edu",
        "Jose L. Melendez": "Special Assistant to the Chancellor\nFull Time Professor\njose.melendez37@upr.edu",
        "Jaime Seguel": "Retired\njaime.seguel@upr.edu",
        "Juan O. Lopez Gerena": "Instructor\njuano.lopez@upr.edu"
    }

    ece_faculty = {
        "Gerson Beauchamp": "Full Time Professor\ngerson.beauchamp@upr.edu",
        "Jaime Arbona Fazzi": "Full Time Professor\njaime.arbona@upr.edu",
        "Jose Cedeño": "AFull Time Professor\njose.cedeno3@upr.edu",
        "Isidoro Couvertier": "Full Time Professor\nisidoro.couvertiero@upr.edu",
        "Shawn David Hunt": "Full Time Professor\nshawndavid.hunt@upr.edu",
        "Henrick Ierick": "Full Time Professor\nhenrick.ierick@upr.edu",
        "Rogelio Palomera ": "Full Time Professor\nrogelio.palomera@upr.edu",
        "Manuel Jimenez": "Full Time Professor\nmanuel.jimenez@upr.edu",
        "Nayda Santiago Santiago": "Full Time Professor\nnayda.santiago@upr.edu",
        "Hamed Parsiani Gobadi": "Full Time Professor\nhamed.parsiani@upr.edu",
        "Guillermo Serrano": "Full Time Professor\nguillermo.serrano.@upr.edu"
    }
    if len(sections) <= 1:
        return 'Por favor, especifica abreviacion del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!dept:inso"'

    department_name: str = sections[1].lower()
    embed = None
    if department_name in ('inso', 'ciic'):
        embed = discord.Embed(title="Facultad CSE",
                              description="")
        embed.add_field(name="Para más contacos de Facultad",
                        value="https://www.uprm.edu/cse/faculty/")
        for name, role in cse_faculty.items():
            embed.add_field(name=name, value=role)

    elif department_name in ('inel', 'icom'):
        embed = discord.Embed(title="Facultad ECE",
                              description="")

        embed.add_field(name="Para más contacos de Facultad",
                        value="https://ece.uprm.edu/people/faculty/#cn-top")
        for name, role in ece_faculty.items():
            embed.add_field(name=name, value=role)

    else:
        embed = "No reconozco ese departamento :eyes: :confused:\n"\
            "Intenta con: INEL, ICOM, INSO o CIIC"
    return embed


def get_consejeria_academica(sections):
    if len(sections) <= 1:
        return 'Por favor, especifica abreviacion del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!consejeroacad:inel"'

    dept_name = sections[1]
    embed: discord.Embed = None
    if dept_name.lower() in ('inel', 'icom'):
        embed = discord.Embed(
            title='Consejeria Academica del Departamento de INEL/ICOM')
        ece_cons = consejeria_profesional.ECEConsejerosProfesional()

        generate_embed(ece_cons, embed)

        embed.remove_field(0)
        embed.insert_field_at(
            index=0,
            name='Servicio',
            value=ece_cons.contact_name
        )

        embed.add_field(
            name='Sistema de reserva de citas ECE',
            value=ece_cons.appointment_system_link
        )
        divisor = '\n\u2022 '
        brochure_list = f'\u2022 {divisor.join(ece_cons.brochures)}'
        embed.add_field(
            name='Folletos Informativos',
            value=brochure_list
        )

        embed.add_field(
            name='Más Información',
            value=ece_cons.more_info
        )
    elif dept_name.lower() in ('inso', 'ciic'):
        embed = discord.Embed(
            title='Consejeria Academica del Departamento de INSO/CIIC')
        cse_cons = consejeria_profesional.CSEConsejerosProfesional()

        generate_embed(cse_cons, embed)

        embed.remove_field(0)
        embed.insert_field_at(
            index=0,
            name='Servicio',
            value=cse_cons.contact_name
        )

        embed.add_field(
            name='Cuando Puedo Ir al Departamento?',
            value="Cuando quieras! Siempre y cuando Celines o uno de los directores este para atenderte y no esten ocupados"
        )
        divisor = '\n\u2022 '
        #CSE DOESNT HAVE BROCHURES
        embed.add_field(
            name='CSE Dept. Website',
            value= cse_cons.brochures[0] #website link
        )

        embed.add_field(
            name= 'Más Información',
            value=cse_cons.more_info
        )
    else:
        return 'Los siento, no reconozco ese departamento. :flushed:\n'\
            'Intenta con: **INSO, INEL, CIIC o ICOM.**'

    return embed


def get_dept_cons_picologicos(sections):
    embed = discord.Embed(
        title='Información de Departamento de Consejería y Servicios Psicológicos (DCSP)')
    dcsp = servicios.ConsejeriaServiciosPsicologicos()
    generate_embed(dcsp, embed)
    embed.add_field(
        name='Pagina Oficial',
        value=dcsp.official_website
    )

    divisor = '\n\u2022 '
    links_list = f'\u2022 {divisor.join(dcsp.enlaces_rapidos)}'
    embed.add_field(
        name='Enlaces Rapidos',
        value=links_list
    )
    embed.add_field(
        name='Contactanos',
        value=dcsp.contatanos
    )

    content_response = dcsp.mensaje_muy_importante
    return {
        'embed': embed,
        'content': content_response
    }


def get_decanato_estudiante(sections):
    embed = discord.Embed(
        title='Información de Departamento del Decanato de Estudiantes')
    decanato = servicios.DecanatoEstudiantes()
    generate_embed(decanato, embed)
    embed.add_field(
        name='Pagina Web',
        value=decanato.website
    )

    divisor = "\n\u2022 "
    social_media_list = f'\u2022 {divisor.join(decanato.social_media)}'
    embed.add_field(
        name="Redes Sociales",
        value=social_media_list
    )

    return embed


_telephone_guide_list = dict(
    {
        '!rectoria': {'func': None, 'description': 'Informacion de Contacto de Rectoria'},
        '!dept': {'func': get_dept_info, 'description': 'Obtener informacion de contacto de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!contactos': {'func': get_telephone_guide_help, 'description': 'Obtener lista completa de contactos disponibles'},
        '!aecon': {'func': get_asistencia_econ, 'description': 'Informacion de Contacto de Asistencia Economica'},
        '!facultad': {'func': get_faculty, 'description': 'Obtener informacion de contacto de la facltad de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!guardia': {'func': get_guardia_universitaria, 'description': 'Informacion de la guardia universitaria'},
        '!consejeroacad': {'func': get_consejeria_academica, 'description': 'Obtener informacion de Asesoría Académica y Consejería Profesional de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!dcsp': {'func': get_dept_cons_picologicos, 'description': 'Informacion del Departamento de Consejería y Servicios Psicológicos (DCSP)'},
        '!dec_estudiantes': {'func': get_decanato_estudiante, 'description': 'Obtener infomacion del Decanato de Estudiantes'},
        '!univa': {'func': None, 'description': 'Informacion sobre Univ Avanzado'},
        '!rectoria': {'func': None, 'description': 'Obtener infomacion Rectoria'}
    }
)


def get_guide_handler(sections):
    sect = sections[0].lower()
    return _telephone_guide_list.get(sect)['func']


def is_command(sections):
    return len(sections) > 0 and sections[0] in _telephone_guide_list
