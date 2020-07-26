"""
//
//  building_parser.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""

import log
import discord
import re

_buildings_list = dict(
    {
        'ae': {'name': 'Administración de Empresas', 'gmaps_loc': 'https://goo.gl/maps/HfgdcA5krWJ1YNnw5'},
        'ai': {'name': 'Antiguo Instituto', 'gmaps_loc': ''},
        'am': {'name': 'Ingeniería Agrícola', 'gmaps_loc': 'https://goo.gl/maps/7bp1WLZQcywqXhSx6'},
        'ap': {'name': 'Anexo Piñero', 'gmaps_loc': ''},
        'ar': {'name': 'Artes Plásticas', 'gmaps_loc': 'https://goo.gl/maps/rJFtqVEWZkpnXk8d6'},
        'az': {'name': 'Finca Alzamora', 'gmaps_loc': 'https://goo.gl/maps/zpFFjM4yVxNmJSkQ6'},
        'b': {'name': 'Biología', 'gmaps_loc': 'https://goo.gl/maps/7N8xgiLTdPLe8S8V6'},
        'c': {'name': 'Celis', 'gmaps_loc': 'https://goo.gl/maps/k8R8Dk8MgyhfJJ2g8'},
        'ca': {'name': 'Campo Atlético', 'gmaps_loc': ''},
        'cd': {'name': 'Centro de Investigación y Desarrollo (CID)', 'gmaps_loc': 'https://goo.gl/maps/3Aw264R5t3FFrVyi8'},
        'ch': {'name': 'Chardón', 'gmaps_loc': 'https://goo.gl/maps/TmA7yS3H42ZyRGkW7'},
        'ci': {'name': 'Ingeniería Civil', 'gmaps_loc': 'https://goo.gl/maps/tTNRYVU5s6if5XzN7'},
        'cm': {'name': 'Coliseo Mangual', 'gmaps_loc': 'https://goo.gl/maps/D453YiKwuBAGdoNJ6'},
        'cs': {'name': 'Cancha Softball', 'gmaps_loc': 'https://goo.gl/maps/KmozoavfMFKs89DK7'},
        'ct': {'name': 'Cancha de Tenis', 'gmaps_loc': 'https://goo.gl/maps/EpPo79fjamwnbZvR8'},
        'ea': {'name': 'Estudios Aeroespaciales', 'gmaps_loc': ''},
        'ee': {'name': 'Edificio de Enfermería', 'gmaps_loc': 'https://goo.gl/maps/agiMtNENRKzam61m6'},
        'ei': {'name': 'Estación de Isabela', 'gmaps_loc': 'https://goo.gl/maps/M3SWq6CwWRRWvUR38'},
        'el': {'name': 'Estación de Lajas', 'gmaps_loc': 'https://goo.gl/maps/ZpQu6wsxvnZ7Qbq48'},
        'en': {'name': 'Laboratorio de Entomología', 'gmaps_loc': ''},
        'ep': {'name': 'Escuela Pública', 'gmaps_loc': ''},
        'f': {'name': 'Física', 'gmaps_loc': 'https://goo.gl/maps/mTX7tjLDQK8zzc5W6'},
        'fi': {'name': 'Otras Fincas', 'gmaps_loc': ''},
        'ge': {'name': 'Gimnasio Ángel F. Espada', 'gmaps_loc': 'https://goo.gl/maps/qiggcfNzY9d9ayf16'},
        'ho': {'name': 'Hospital', 'gmaps_loc': ''},
        'ib‐1': {'name': 'Salones de Instrucción Bibliotecaria', 'gmaps_loc': 'https://goo.gl/maps/8R8vbd7b292UaCEs8'},
        'ib‐2': {'name': 'Biblioteca General', 'gmaps_loc': 'https://goo.gl/maps/8R8vbd7b292UaCEs8'},
        'ii': {'name': 'Ingeniería Industrial', 'gmaps_loc': 'https://goo.gl/maps/fX4iWoPuk9sWwjHWA'},
        'ic': {'name': 'Invernadero de Protección de Cultivos', 'gmaps_loc': ''},
        'ih': {'name': 'Invernadero de Horticultura', 'gmaps_loc': ''},
        'ip': {'name': 'Invernadero de Industria Pecuaria', 'gmaps_loc': ''},
        'iq': {'name': 'Ingeniería Química', 'gmaps_loc': 'https://goo.gl/maps/cxyNkdJyKYz8pJ9a8'},
        'l': {'name': 'Antonio Lucchetti (Ingeniería Mecánica)', 'gmaps_loc': 'https://goo.gl/maps/2Pdd75AnZ8bUzUV26'},
        'm': {'name': 'Luis Monzón (Matemáticas)', 'gmaps_loc': 'https://goo.gl/maps/UrivXZeNRZvKN5bk6'},
        'mi': {'name': 'Miradero (Artes Plásticas)', 'gmaps_loc': ''},
        'mg': {'name': 'Isla Magueyes', 'gmaps_loc': ''},
        'p': {'name': 'Jesús T. Piñero (Agricultura)', 'gmaps_loc': 'https://goo.gl/maps/VyjFoe38QbExcUJXA'},
        'pa': {'name': 'Piscina Alumni', 'gmaps_loc': 'https://goo.gl/maps/eQqX8kMneSY2qaAN8'},
        'ps': {'name': 'Pista Sintética', 'gmaps_loc': 'https://goo.gl/maps/R2rVsaxbTDffUygw7'},
        'q': {'name': 'Química', 'gmaps_loc': 'https://goo.gl/maps/jxNcnEnb8sgdKAbq6'},
        'ra': {'name': 'Alfredo Ramírez de Arellano y Rosell', 'gmaps_loc': 'https://goo.gl/maps/gxNiSYZWM9nKTyMo7'},
        's': {'name': 'Luis Stefani (Ingeniería)', 'gmaps_loc': 'https://goo.gl/maps/6ZJ5nwEkPRvYVVWf6'},
        'sa': {'name': 'Sánchez Hall(ROTC)', 'gmaps_loc': 'https://goo.gl/maps/Eeww5ub5EFvqwZDXA'},
        'sh': {'name': 'Efraín Sánchez Hidalgo (Economía y PPMES)', 'gmaps_loc': 'https://goo.gl/maps/pWULVaha3M74dffy9'},
        't': {'name': 'Terrats (Pagaduría y Finanzas)', 'gmaps_loc': 'https://goo.gl/maps/Rsto52FzgRVCoFdP6'},
        'ta': {'name': 'Taller de Artes Gráficas', 'gmaps_loc': 'https://goo.gl/maps/DsqsGe5ezfaP6mBi7'}
    }
)


def is_valid_room_number(sections):
    if len(sections) == 1:
        return False

    tmp = sections[1]

    regex_result = re.findall("^\D+", tmp)

    if len(regex_result) == 1:
        return True

    return False


def get_building_information(sections):
    information = None
    if len(sections) == 1:
        return False

    salon = sections[1]

    salon_splited = re.split('-', salon)

    regex_result = re.findall("^\D+", salon_splited[0])

    if len(regex_result) != 1:
        return False

    text_part_of_code: str = regex_result[0].lower()

    log.debug(f'avdv {text_part_of_code}')

    if text_part_of_code in _buildings_list:
        return _buildings_list[text_part_of_code]
    else:
        return False
