import discord
import log


def help_menu_base():
    log.debug('[DEBUG] Enter Counselor Help')
    embed = discord.Embed(title="Lista de Commandos")

    embed.add_field(name="!help",
                    value="Mostrara la lista de los commandos disponibles.")
    embed.add_field(name="!curriculo:DEPT",
                    value="Te proveéra un PDF del curriculo del DEPT (INEL/ICOM/INSO/CIIC)")
    embed.add_field(
        name="!map", value="Provee un enlace a el Mapa de UPRM")
    embed.add_field(
        name="!links", value="Gives the user a PDF with all the important links of UPRM")
    embed.add_field(
        name="!emails", value="Gives user a PDF with some important emails they can use")
    embed.add_field(
        name="!salon:CODIGO_SALON", value="Provee información sobre el DEPT(INEL/ICOM or INSO/CIIC).\n"
        "Ejemplo: *!salon:S123*.\tSi el salón comienza con una letra entonces debe dividir la letra que identifica al edificio y el numero del salón con un guión (-).\n"
        "Ejemplo: *!salon:F-B*, este es el Anfiteatro B del edificio de Física"
    )
    embed.add_field(
        name='!contactos',
        value='Mostrara una lista de todos los contactos que tengo disponible para ofrecerte.'
    )
    embed.add_field(
        name="!dept:DEPT", value="Provee información sobre el DEPT (INEL/ICOM or INSO/CIIC).\n"
        "Localización de la oficina, horas de trabajo, numero de teléfono, extensión, etc."
    )
    embed.add_field(
        name="!facultad:DEPT",
        value="Provee información de contacto para facultad del DEPT (INEL/ICOM/INSO/CIIC).\n"
    )
    embed.add_field(
        name='!guardia',
        value='Provee informacion de la guardia universitaria, policia estatal y otros servicios de emergencia regionales.'
    )
    return embed


def help_menu_for_prepa():
    return help_menu_base()


def help_menu_for_counselor():
    return help_menu_base()


def help_menu_join():
    return help_menu_base()
