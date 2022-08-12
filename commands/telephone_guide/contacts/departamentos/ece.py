"""
//  /handlers/telephone_guide/contacts/departamentos/ece.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/24/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""

from ..contact import Contact


class ECEDepartment(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    #"""

    def __init__(self):
        contact_name = "Departamento de Ingeniería Electrica y de Computadoras"
        contact_description = (
            "Información, contactos y horario del departamento de INEL-ICOM"
        )
        services_provided = (
            "Multiples servicios para estudiantes en el departamento de INEL-ICOM"
        )
        phone_number = ["(787) 832-4040"]
        extensions = [
            "Ext. 3086",
            "Ext. 3821",
            "Ext. 3090",
            "Ext. 3094",
            "Ext. 3121",
            "Ext. 2170",
        ]
        emails = ["director.inec@uprm.edu"]
        office_number = "Edificio Stefani - Oficina 125A"
        owner = None
        work_hours = "Lunes - Viernes | 7:30 AM - 11:30 AM & 1:30 PM - 4:30 PM"
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
