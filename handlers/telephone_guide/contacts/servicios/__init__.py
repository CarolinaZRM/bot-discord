'''
//  /handlers/telephone_guide/contacts/servicios/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''

from .dean_of_students import DecanatoEstudiantes
from .economic_assistance import AsistenciaEconomica
from .psycological_counseling import ConsejeriaServiciosPsicologicos
from .university_guard import GuardiaUniversitaria

__all__ = [
    DecanatoEstudiantes,
    AsistenciaEconomica,
    ConsejeriaServiciosPsicologicos,
    GuardiaUniversitaria,
]
