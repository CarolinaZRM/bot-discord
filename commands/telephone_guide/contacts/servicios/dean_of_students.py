"""
//  /handlers/telephone_guide/contacts/servicios/dean_of_students.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
"""
from ..contact import Contact


class DecanatoEstudiantes(Contact):
    def __init__(self):
        contact_name = "Oficina Virtual Del Decano De Estudiantes"
        contact_description = (
            "Proveer al estudiante los recursos y servicios necesarios para contribuir a"
            " su desarrollo físico, social, emocional, cultural, educativo y"
            " ocupacional-profesional, como complemento a su formación intelectual,"
            " académica y ética."
        )
        services_provided = (
            "\u2022 Acomodo Razonable\n"
            "\u2022 Recomendación Del Decano\n"
            "\u2022 Apelación De Beca\n"
            "\u2022 Reglamento De Estudiantes Del Rum\n"
            "\u2022 Certificación De Progreso Académico\n"
            "\u2022 Protocolo De Excusas"
        )
        phone_number = ["(787) 265-3862"]
        extensions = None
        emails = ["decano.estudiantes@uprm.edu"]
        office_number = "1er Piso"
        owner = None
        work_hours = "Lunes – Viernes | 7:45AM - 4:30PM"
        gmaps_location = "https://goo.gl/maps/4o7eRkwZu6yoUhVv9"
        super().__init__(
            contact_name,
            contact_description,
            services_provided,
            phone_number,
            extensions=extensions,
            emails=emails,
            office_number=office_number,
            owner=owner,
            work_hours=work_hours,
            gmaps_location=gmaps_location,
        )
        self.website = "https://www.uprm.edu/decestu/"
        self.social_media = [
            "Twitter - @EstudiantesUPRM | https://twitter.com/EstudiantesUPRM?lang=en",
            "Youtube - Prensa RUM | https://www.youtube.com/user/videocolegio",
            "Facebook - Decanato De Estudiantes Uprm |"
            " https://www.facebook.com/decano.estudiantes/",
        ]
