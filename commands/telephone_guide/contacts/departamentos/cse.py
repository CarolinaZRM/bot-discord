"""
//  /handlers/telephone_guide/contacts/departamentos/cse.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/24/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
from ..contact import Contact


class CSEDepartment(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    #"""

    def __init__(self):
        contact_name = (
            "Departamento de Ingenieria de Software & Ciencias de la Computación"
        )
        contact_description = (
            "Información, contactos y horario del departamento de INSO-CIIC"
        )
        services_provided = (
            "Multiples servicios para estudiantes en el departamento de INSO-CIIC"
        )
        phone_number = ["(787) 832-4040"]
        extensions = [
            "Ext. 5864 (Acting Director – Dr. Pedro I. Rivera Vega)",
            "Ext. 5864 (Associate Director – Dr. Manuel Rodriguez Martinez)",
            "Ext. 5997 (Student Affairs Officer - Celines Alfaro Almeyda",
            "Ext. 5864 & 6476 Administrative Officer – Sarah Ferrer)",
            "Ext. 5864 (Administrative Secretary – Gedyeliz Zoe Valle)",
        ]
        emails = [
            "p.rivera@upr.edu",
            "manuel.rodriguez7@upr.edu",
            "celines.alfaro@upr.edu",
            "gedyeliz.valle@upr.edu",
        ]
        office_number = "Edificio Stefani - Oficina 220"
        owner = None
        work_hours = "Lunes - Viernes | 7:30 AM - 11:30 AM & 1:30 PM - 4:30 PM"
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
        )
