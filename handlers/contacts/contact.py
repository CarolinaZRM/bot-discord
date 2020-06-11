# from typing import List

class Contact():
    """
    Anadir los numeros con descripcion de el contacto y/o la oficina
    De aplicar el numero deberia tener la siguiente informacion:
    - Nombre de la oficina
    - Numero de telefono
    - Extension: can be a list
    - Que servicios ofrecen, proposito para el cual se deberia llamar
    - Persona a la que pertenece esa extension (si aplica)
    """

    def __init__(self, contact_name, contact_description, services_provided,
                 phone_number, extensions=[],
                 emails=[], office_number='Unavailable',
                 owner='Unavailable', work_hours: str = 'Unavailable', gmaps_location='Unavailable'):
        super().__init__()
        self.contact_name = contact_name
        self.phone_number = phone_number
        self.contact_description = contact_description
        self.extensions = extensions
        self.services_provided = services_provided
        self.emails = emails
        self.owner = owner
        self.office_number = office_number
        self.work_hours = work_hours
        self.gmaps_location = gmaps_location

    def __str__(self):
        email_txt = ', '.join(self.emails)
        phone_txt = ', '.join(self.phone_number)
        extensions_txt = ' \u2022 '.join(self.extensions)

        extensions_bullet_list = ''

        return_string = f'''Contact Name: {self.contact_name}
    \u2022 Contact description: {self.contact_description}
    \u2022 Service Provided: {self.services_provided}
    \u2022 Office: {self.office_number}
    \u2022 Phones: {phone_txt}
    \u2022 Phone Extensions: {extensions_txt}
    \u2022 Work Hours: {self.work_hours}
    \u2022 Google Maps Location: {self.gmaps_location}'''
        return return_string
