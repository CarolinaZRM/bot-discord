'''
//  /handlers/telephone_guide/contacts/servicios/university_guard.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
from ..contact import Contact


class GuardiaUniversitaria(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    # """

    def __init__(self):
        contact_name = "Dpto. De Transito Y Vigilancia"
        contact_description = "<Add Description>"
        services_provided = "<Add services provided>"
        phone_number = ["(787) 832-4040"]
        extensions = ["Retén Exts. 3263,3620",
                      "Sección de Tránsito – Exts. 3275,3597",
                      'Oficina Director – Exts. 2462, 3538, 2458']
        emails = ['transito@uprm.edu']
        office_number = "Vagones al costado del Edificio del Dpto. de Enfermería"
        gmaps_location = "https://goo.gl/maps/q1poMfAh7rthfDah8"
        owner = None
        work_hours = "Lunes a Viernes | 7:45 A.M. a 11:45 A.M. | 1:00 P.M. a 4:30 P.M."
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)
        self.additional_helpful_info = ['Emergencias Médicas Municipal y Bomberos 787-834-8585 | Exts. 2061/2062',
                                        'Línea Directa: 787-265-1785/787-265-3872',
                                        "Policía Estatal 787-832-2020 (Linea Confidencial)/787-832-9696 (Comandancia Estatal)",
                                        "Policía Municipal 787-834-8585 Ext. 2025"]
        self.more_info_link = 'https://www.uprm.edu/transitoyvigilancia/'
