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
        office_number = "Lobby Decanato de Estudiantes"
        gmaps_location = "https://goo.gl/maps/q1poMfAh7rthfDah8"
        owner = None
        work_hours = "Lunes a Viernes | 7:45 A.M. a 11:45 A.M. | 1:00 P.M. a 4:30 P.M."
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)
        self.emergencias_medicas = 'Emergencias Médicas Municipal y Bomberos 787-834-8585 | Exts. 2061/2062'
        self.linea_directa = 'Línea Directa: 787-265-1785/787-265-3872'
        self.policia_estatal = "Policia Estatal 787-832-2020 (Linea Confidencial)/787-832-9696 (Comandancia Estatal)"
        self.policia_municipal = "Policia Municipal 787-834-8585 Ext. 2025"
        self.more_info_link = 'https://www.uprm.edu/transitoyvigilancia/'
