from handlers.contacts.contact import Contact


class ECEDepartment(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    # """

    def __init__(self):
        contact_name = "Electrical and Computer Engineering Department"
        contact_description = "This is the Electrical and Computer Engineering Department (INEL/ICOM)"
        services_provided = "<Add services provided>"
        phone_number = ["(787) 832-4040"]
        extensions = ["Ext. 3086", "Ext. 3821", "Ext. 3090",
                      "Ext. 3094", "Ext. 3121", "Ext. 2170"]
        emails = ["director.inec@uprm.edu"]
        office_number = "Stefani Building - Office 125A"
        owner = None
        work_hours = '7:30 AM - 11:30 AM & 1:30 PM - 4:30 PM'
        gmaps_location = 'https://goo.gl/maps/Jb43w1iy2VfjMeSR6'
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours, gmaps_location=gmaps_location)


class CSEDepartment(Contact):
    """[summary]

    Args:
        Contact ([type]): [description]
    # """

    def __init__(self):
        contact_name = "Computer Science & Engineering Department"
        contact_description = "This is the Computer Science & Engineering Department (INSO/CIIC)"
        services_provided = "<Add services provided>"
        phone_number = ["(787) 832-4040"]
        extensions = [
            "Ext. 5864 (Acting Director – Dr. Pedro I. Rivera Vega)",
            "Ext. 5864 (Associate Director – Dr. Manuel Rodriguez Martinez)",
            "Ext. 5997 (Student Affairs Officer - Celines Alfaro Almeyda",
            "Ext. 5864 & 6476 Administrative Officer – Sarah Ferrer)",
            "Ext. 5864 (Administrative Secretary – Gedyeliz Zoe Valle)"]
        emails = ["p.rivera@upr.edu", "manuel.rodriguez7@upr.edu",
                  "celines.alfaro@upr.edu", "gedyeliz.valle@upr.edu"]
        office_number = "S-220 (Stefani Building)"
        owner = None
        work_hours = '7:30 AM - 11:30 AM & 1:30 PM - 4:30 PM'
        super().__init__(contact_name, contact_description, services_provided,
                         phone_number, extensions=extensions,
                         emails=emails, office_number=office_number,
                         owner=owner, work_hours=work_hours)
