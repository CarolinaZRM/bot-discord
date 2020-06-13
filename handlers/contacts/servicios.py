from handlers.contacts.contact import Contact


class AsistenciaEconomica(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    # """

    def __init__(self):
        contact_name = "Oficina de Asistencia Economica"
        contact_description = "<Add Description>"
        services_provided = "<Add services provided>"
        phone_number = ["(787) 832-4040"]
        extensions = ["Ext. 3863"]
        emails = []
        office_number = "Lobby Decanato de Estudiantes"
        gmaps_location = "https://goo.gl/maps/pyAjRnaKZ1gE99PA7"
        owner = None
        work_hours = "Lunes a Viernes | 7:45 – 11:45 A.M. | 1:00 – 4:30 P.M."
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)
        self.important_dates_link = 'https://www.uprm.edu/asistenciaeconomica/fechas-importantes/'

    def __str__(self):
        return f'{super().__str__()}\n\n'\
            f'Aqui puedes encontrar las fechas importantes de Asistencia Economica:\n{self.important_dates_link}'


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
                                        "Policia Estatal 787-832-2020 (Linea Confidencial)/787-832-9696 (Comandancia Estatal)",
                                        "Policia Municipal 787-834-8585 Ext. 2025"]
        self.more_info_link = 'https://www.uprm.edu/transitoyvigilancia/'


class ConsejeriaServiciosPsicologicos(Contact):
    def __init__(self):
        contact_name = "Departamento de Consejería y Servicios Psicológicos(DCSP)"
        contact_description = "El Departamento de Consejería y Servicios Psicológicos (DCSP) es una unidad docente, "\
            "adscrita al Decanato de Estudiantes del Recinto Universitario de Mayagüez de la Universidad "\
            "de Puerto Rico."
        services_provided = "\u2022 Consejería individual y grupal\n"\
            "\u2022 Psicoterapia individual y grupal\n"\
            "\u2022 Administración e interpretación de inventarios de intereses vocacionales\n"\
            "\u2022 Consultoría\n"\
            "\u2022 Grupos de Apoyo\n"
        phone_number = ['(787) 265 3864']
        extensions = None
        emails = ['DCSP@uprm.edu']
        office_number = 'Centro de Estudiantes - Oficina 501 (5to piso)'
        owner = None
        work_hours = 'Lunes – Viernes | 7:30 AM – 4:30 PM'
        gmaps_location = 'https://goo.gl/maps/VQNoPR3qRsPoicJz8'
        super().__init__(contact_name, contact_description, services_provided, phone_number, extensions=extensions,
                         emails=emails, office_number=office_number, owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)

        self.official_website = 'https://www.uprm.edu/dcsp/'
        self.contatanos = 'https://www.uprm.edu/dcsp/contactanos/'

        self.mensaje_muy_importante = "**Fuera de horas laborables:**\n"\
            "Nuestros profesionales de ayuda no están disponibles fuera de horas laborales. Si la situación es tal que "\
            "no puede esperar a ser atendida el próximo día laboral, puedes usar los siguientes recursos en la "\
            "comunidad que tienen líneas de ayuda 24 horas:\n\n"\
            "**Líneas de Ayuda**\n"\
            "\u2022 Línea PAS (Primera Ayuda Psicosocial): 1-800-981-0023\n"\
            "\u2022 Sistema 911\n"\
            "\u2022 Suicide Prevention Life Line 1-888-628-9454\n"\
            "\u2022 Centro de Ayuda a Víctimas de Violación 1-800-981-5721\n"\
            "\u2022 Control de Envenenamiento 1-800-222-1222\n\n"\
            "**Clínicas de Salud Mental**\n"\
            "\u2022 Centro de Salud Conductual Menonita CIMA 1-800-981-1218\n"\
            "\u2022 Clínicas Ambulatorias de APS (Vital) 787-641-9133\n"\
            "\u2022 Hospital Metro Pavia- Salud Conductual 787-851-0833\n"\
            "\u2022 Hospital Panamericano: 1-800-981-1218\n"\
            "\u2022 Sistema San Juan Capestrano: 787-760-0222"
