import discord
from handlers.contacts import departamentos, servicios


def get_dept_info(sections):

    if len(sections) <= 1:
        return 'Porfavor especifica abreviacion del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!dept:inso"'

    departartment_name: str = sections[1].lower()

    return_message = f"Aqui esta la informacion de '{departartment_name.upper()}':\n\n"

    if departartment_name in ('inso', 'ciic'):
        return_message = f'{return_message}\n\n1. {departamentos.InsoDepartment()}'
    elif departartment_name in ('icom', 'inel'):
        return_message = f'{return_message}1. {departamentos.IcomDepartment()}'
    else:
        return_message = f'Departamento invalido.'

    return return_message


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


_telephone_guide_list = dict(
    {
        '!rectoria': {'func': None, 'description': 'Informacion de Contacto de Rectoria'},
        '!dept': {'func': get_dept_info, 'description': 'Obtener informacion de contacto de los departamentos de INEL/ICOM/INCO/CIIC'},
        '!contactos': {'func': get_telephone_guide_help, 'description': 'Obtener lista completa de contactos disponibles'},
        '!aecon': {'func': get_asistecia_econ, 'description': 'Informacion de Contacto de Asistencia Economica'}
    }
)


_help_msg = 'Las listas de telefonos son:\n'


def get_guide_handler(sections):
    sect = sections[0].lower()
    return _telephone_guide_list.get(sect)['func']


def is_command(sections):
    return len(sections) > 0 and sections[0] in _telephone_guide_list
