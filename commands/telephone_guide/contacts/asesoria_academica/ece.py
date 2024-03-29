"""
//  /handlers/telephone_guide/contacts/asesoria_academica/ece.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/24/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

from ..contact import Contact


class ECEAsesoriaAcademica(Contact):
    def __init__(self):
        contact_name = "Asesoria Académica INEL/ICOM"
        contact_description = (
            "Ayudar y dirigir al estudiante en la planificación de su programa"
            " académico, para que cumpla con los requisitos de graduación y pueda así,"
            " completar su grado académico."
        )
        services_provided = (
            "Asesoría y evaluación semestral o anual a los estudiantes en procesos de:"
            " matrícula, admisión, reclasificación, traslado, permiso especial,"
            " readmisión, transferencias, baja parcial, baja total, bajo aprovechamiento"
            " académico (probatorias, suspensiones) y graduación."
        )
        phone_number = ["(787) 832-4040", "FAX: (787) 831-7564"]
        extensions = ["Ext. 3182"]
        emails = ["veronica.vazquez1@upr.edu", "maritza.figueroa@ece.uprm.edu"]
        office_number = "Stefani Building - Office 224"
        owner = None
        work_hours = "Lunes-Viernes | 7:30 AM - 11:30 AM & 1:30 PM - 4:30 PM"
        gmaps_location = "https://goo.gl/maps/Jb43w1iy2VfjMeSR6"
        super().__init__(
            contact_name,
            contact_description,
            services_provided,
            phone_number,
            extensions=extensions,
            emails=emails,
            office_number=office_number,
            owner=owner,
            work_hours=work_hours,
            gmaps_location=gmaps_location,
        )
        self.appointment_system_link = "https://appointments.ece.uprm.edu/"
        self.brochures = [
            "Español -"
            " https://ece.uprm.edu/wp-content/uploads/Brochure-INEL-ICOM-Spanish-Rev.-2015.pdf",
            "English -"
            " https://ece.uprm.edu/wp-content/uploads/Brochure-INEL-ICOM-English-Rev.-2014.pdf",
        ]
        self.more_info = "https://www.uprm.edu/asuntosacademicos/orientacion-academica-y-consejeria-profesional/"
        self.asesoria_uprm = "https://www.uprm.edu/asuntosacademicos/orientacion-academica-y-consejeria-profesional/"
