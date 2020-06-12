import discord
from handlers.contacts import departamentos, servicios


def get_dept_info(sections):

    if len(sections) <= 1:
        return 'Porfavor especifica abreviacion del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!dept:inso"'

    departartment_name: str = sections[1].lower()

    #return_message = f"Aqui esta la informacion de '{departartment_name.upper()}':\n\n"
    embed = None
    if departartment_name in ('inso', 'ciic'):
        cse = departamentos.CSEDepartment()
        embed = discord.Embed(title="CSE Department Info",
                              description="Useful CSE department information")
        embed.add_field(name="Dept. Name", value=cse.contact_name)
        embed.add_field(name="Dept. Description",
                        value=cse.contact_description)
        embed.add_field(name="Services Provided", value=cse.services_provided)
        embed.add_field(name="Office", value=cse.office_number)

        divisor = '\n\u2022 '
        phone_list = f"\u2022 {divisor.join(cse.phone_number)}"

        embed.add_field(name="Phones", value=phone_list)

        extension_list = f"\u2022 {divisor.join(cse.extensions)}"
        embed.add_field(name="Extension", value=extension_list)

        embed.add_field(name="Work Hours", value=cse.work_hours)
        embed.add_field(name="Google Maps Location", value=cse.gmaps_location)

        return embed
        #return_message = f'{return_message}\n\n1. {departamentos.CSEDepartment()}'
    elif departartment_name in ('icom', 'inel'):
        #return_message = f'{return_message}1. {departamentos.ECEDepartment()}'

        ece = departamentos.ECEDepartment()
        embed = discord.Embed(title="ECE Department Info",
                              description="Useful ECE department information")
        embed.add_field(name="Dept. Name", value=ece.contact_name)
        embed.add_field(name="Dept. Description",
                        value=ece.contact_description)
        embed.add_field(name="Services Provided", value=ece.services_provided)
        embed.add_field(name="Office", value=ece.office_number)

        divisor = '\n\u2022 '
        phone_list = f"\u2022 {divisor.join(ece.phone_number)}"
        embed.add_field(name="Phones", value=phone_list)

        extension_list = f"\u2022 {divisor.join(ece.extensions)}"
        embed.add_field(name="Extension", value=extension_list)
        embed.add_field(name="Work Hours", value=ece.work_hours)
        embed.add_field(name="Google Maps Location", value=ece.gmaps_location)

        return embed
    else:
        embed = "Departamento Invalido"
        #return_message = f'Departamento invalido.'

    return embed


def get_asistecia_econ(section):
    return_message = "Aqui esta la informacion de la Oficina de Asistencia Economica:\n\n"
    return f'{return_message}1. {servicios.AsistenciaEconomica()}'


def get_telephone_guide_help(sections):
    telefone_list_keys = set()
    for key in _telephone_guide_list:
        if _telephone_guide_list[key]['func']:
            msg = f'{key}: {_telephone_guide_list[key]["description"]}'
            telefone_list_keys.add(msg)
    joiner = "\n\t\u2022 "
    response = f'{_help_msg}\t\u2022 {joiner.join(telefone_list_keys)}'
    return response


def get_faculty(sections):
    pass


_telephone_guide_list = dict(
    {
        '!rectoria': {'func': None, 'description': 'Informacion de Contacto de Rectoria'},
        '!dept': {'func': get_dept_info, 'description': 'Obtener informacion de contacto de los departamentos de INEL/ICOM/INSO/CIIC'},
        '!contactos': {'func': get_telephone_guide_help, 'description': 'Obtener lista completa de contactos disponibles'},
        '!aecon': {'func': get_asistecia_econ, 'description': 'Informacion de Contacto de Asistencia Economica'},
        '!faculty': {'func': get_faculty, 'description': 'Obtener informacion de contacto de la facltad de los departamentos de INEL/ICOM/INSO/CIIC'},

    }
)


_help_msg = 'Las listas de telefonos son:\n'


def get_guide_handler(sections):
    sect = sections[0].lower()
    return _telephone_guide_list.get(sect)['func']


def is_command(sections):
    return len(sections) > 0 and sections[0] in _telephone_guide_list
