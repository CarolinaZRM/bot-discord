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
