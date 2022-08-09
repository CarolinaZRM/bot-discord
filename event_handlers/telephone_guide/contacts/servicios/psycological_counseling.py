'''
//  /handlers/telephone_guide/contacts/servicios/psycological_counseling.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
from ..contact import Contact


class ConsejeriaServiciosPsicologicos(Contact):
    def __init__(self):
        contact_name = "Departamento de Consejería y Servicios Psicológicos(DCSP)"
        contact_description = "El Departamento de Consejería y Servicios Psicológicos (DCSP) es una unidad docente, "\
            "adscrita al Decanato de Estudiantes del Recinto Universitario de Mayagüez de la Universidad "\
            "de Puerto Rico."
        services_provided = "\u2022 Consejería individual y grupal\n"\
            "\u2022 Psicoterapia individual y grupal\n"\
            "\u2022 Administración e interpretación de inventarios de intereses vocacionales\n"\
            "\u2022 Consultoría\n"\
            "\u2022 Grupos de Apoyo\n"
        phone_number = ['(787) 265 3864']
        extensions = None
        emails = ['DCSP@uprm.edu']
        office_number = 'Centro de Estudiantes - Oficina 501 (5to piso)'
        owner = None
        work_hours = 'Lunes – Viernes | 7:30 AM – 4:30 PM'
        gmaps_location = 'https://goo.gl/maps/VQNoPR3qRsPoicJz8'
        super().__init__(contact_name, contact_description, services_provided, phone_number, extensions=extensions,
                         emails=emails, office_number=office_number, owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)

        self.official_website = 'https://www.uprm.edu/dcsp/'
        self.contatanos = 'https://www.uprm.edu/dcsp/contactanos/'

        self.enlaces_rapidos = ["Citas & Referidos: https://www.uprm.edu/dcsp/citas-referidos/",
                                "Manejo de Crisis: https://www.uprm.edu/dcsp/manejo-de-crisis-2/",
                                "Consejería Profesional: https://www.uprm.edu/dcsp/consejeria/",
                                "Servicios Psicológicos: https://www.uprm.edu/dcsp/servicios-psicologicos/"]

        self.mensaje_muy_importante = "**Fuera de horas laborables:**\n"\
            "Nuestros profesionales de ayuda no están disponibles fuera de horas laborales.\nSi la situación es tal que "\
            "no puede esperar a ser atendida el próximo día laboral,\npuedes usar los siguientes recursos en la "\
            "comunidad que tienen líneas de ayuda 24 horas:\n\n"\
            "**Líneas de Ayuda**\n"\
            "\u2022 Línea PAS (Primera Ayuda Psicológica): 1-800-981-0023\n"\
            "\u2022 Sistema 911\n"\
            "\u2022 Suicide Prevention Life Line 1-888-628-9454\n"\
            "\u2022 Centro de Ayuda a Víctimas de Violación 1-800-981-5721\n"\
            "\u2022 Control de Envenenamiento 1-800-222-1222\n\n"\
            "**Clínicas de Salud Mental**\n"\
            "\u2022 Centro de Salud Conductual Menonita CIMA 1-800-981-1218\n"\
            "\u2022 Clínicas Ambulatorias de APS (Vital) 787-641-9133\n"\
            "\u2022 Hospital Metro Pavía- Salud Conductual 787-851-0833\n"\
            "\u2022 Hospital Panamericano: 1-800-981-1218\n"\
            "\u2022 Sistema San Juan Capestrano: 787-760-0222"
