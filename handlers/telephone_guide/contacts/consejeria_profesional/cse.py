'''
//  /handlers/telephone_guide/contacts/consejeria_profesional/cse.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/24/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''

from ..contact import Contact


class CSEConsejerosProfesional(Contact):
    def __init__(self):
        contact_name = 'Consejeria Académica INSO/CIIC'
        contact_description = "Ayudar y dirigir al estudiante en la planificación de su programa académico, "\
            "para que cumpla con los requisitos de graduación y pueda así, completar su grado académico."
        services_provided = "Asesoría y evaluación semestral o anual a los estudiantes en "\
            "procesos de: matrícula, admisión, reclasificación, traslado, permiso especial, "\
            "readmisión, transferencias, baja parcial, baja total, bajo aprovechamiento académico (probatorias, suspensiones) y graduación."
        phone_number = ['(787) 832-4040']
        extensions = ['Ext. 5597']
        emails = ['celines.alfaro@upr.edu']
        office_number = 'Stefani Building - Office 220'
        owner = None
        work_hours = 'Lunes-Viernes | 7:30 AM - 11:30 AM & 1:30 PM - 4:30 PM'
        gmaps_location = 'https://goo.gl/maps/Jb43w1iy2VfjMeSR6'
        super().__init__(contact_name, contact_description, services_provided, phone_number, extensions=extensions,
                         emails=emails, office_number=office_number, owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)
        self.appointment_system_link = 'Unavailable'
        self.brochures = [
            'Website - https://cse.uprm.edu'
        ]
        self.more_info = 'https://www.uprm.edu/asuntosacademicos/orientacion-academica-y-consejeria-profesional/'
        self.consejeria_uprm = 'https://www.uprm.edu/asuntosacademicos/orientacion-academica-y-consejeria-profesional/'
