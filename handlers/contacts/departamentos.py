from handlers.contacts.contact import Contact


class IcomDepartment(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    # """

    def __init__(self):
        contact_name = "Eectrical and Computer Engineering Department"
        contact_description = "This is the department of INEL/ICOM"
        services_provided = "<Add services provided>"
        phone_number = ["(787) 832-4040"]
        extensions = ["Ext. 3086", "Ext. 3821", "Ext. 3090",
                      "Ext. 3094", "Ext. 3121", "Ext. 2170"]
        emails = ["director.inec@uprm.edu"]
        office_number = "Stefani Building - Office 125A"
        owner = None
        work_hours = 'Unavailable'
        gmaps_location = 'https://goo.gl/maps/Jb43w1iy2VfjMeSR6'
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)


class InsoDepartment(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    # """

    def __init__(self):
        contact_name = "INSO and Computer Engineering Department"
        contact_description = "This is the department of INEL/ICOM"
        services_provided = "<Add services provided>"
        phone_number = ["(787) 832-4040"]
        extensions = [
            "Ext. 5827 (Acting Director – Bienvenido Velez)",
            "Ext. 5864 (Associate Director – Jaime Seguel)",
            "Ext. 5864 & 6476 (Administrative officer – Sarah Ferrer)",
            "Ext. 5864 (Administrative Secretary – Gedyeliz Valle)"]
        emails = []
        office_number = "Stefani Building – Office 220"
        owner = None
        work_hours = 'Unavailable'
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours)
