'''
//  /handlers/telephone_guide/generate_embed.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''


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
