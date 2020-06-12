import discord
import log
import os
from handlers import telephone_guide, building_parser

CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))

# PDF Files
CURRICULO_INEL = os.path.join(CURRENT_DIR, "res", "curriculos", "INEL.pdf")
CURRICULO_INSO = os.path.join(CURRENT_DIR, "res", "curriculos", "INSO.pdf")
CURRICULO_CIIC = os.path.join(CURRENT_DIR, "res", "curriculos", "CIIC.pdf")
CURRICULO_ICOM = os.path.join(CURRENT_DIR, "res", "curriculos", "ICOM.pdf")
CURRICULO_CIIC_LINK = "https://www.uprm.edu/cse/bs-computer-science-and-engineering-2/"


async def event_get_curriculum(message: discord.Message):
    log.debug('[DEBUG] Entered Curriculum')
    user_message = message.content
    if "!curriculo" in user_message.lower():  # Asked for curriculum
        split = user_message.split(" ")
        log.debug('[DEBUG] Contains Curriculum')
        if len(split) == 1:
            await message.author.send("Tienes que decirme que curriculo quieres! (INEL/ICOM/INSO/CIIC)")
        else:
            if split[1].upper() == "INEL":
                await message.author.send("Here is the Electrical Engineering Curriculum:")
                await message.author.send(file=discord.File(CURRICULO_INEL))
            if split[1].upper() == "ICOM":
                await message.author.send("Here is the Computer Engineering Curriculum:")
                await message.author.send(file=discord.File(CURRICULO_ICOM))
            if split[1].upper() == "INSO":
                await message.author.send("Here is the Software Engineering Curriculum:")
                await message.author.send(file=discord.File(CURRICULO_INSO))
            if split[1].upper() == "CIIC":
                await message.author.send("Here is the Computer Science & Engineering Curriculum:")
                # for when CIIC curriculum is updated
                # await message.author.send(file=discord.File(CURRICULO_CIIC))
                await message.author.send(CURRICULO_CIIC_LINK)


async def event_telephone_guide(message: discord.Message):
    log.debug('[DEBUG] Entered telephone guide')
    client_message: str = message.content
    sections = client_message.split(':')

    if telephone_guide.is_command(sections):
        function_call = telephone_guide.get_guide_handler(sections)
        if function_call:
            response = function_call(sections)

            await message.author.send(response)


async def event_parse_university_building(message: discord.Message):
    client_message: str = message.content
    sections = client_message.split(':')

    user_name = None

    if hasattr(message.author, 'nick'):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    # response = f'Hola {user_name}, Es posible que este salon se encuentre en el edificio:\n'
    log.debug(f'avdadv {sections}')
    if len(sections) > 1 and sections[0] == '!salon' and len(sections[1]) > 0:

        if not building_parser.is_valid_room_number(sections):
            await message.author.send('El codigo del salon no es valido.')
            return

        information = building_parser.get_building_information(sections)

        if information:
            response_msg = f"Hola {user_name}! Es posible que este salon se encuentre en el edificio: **'{information['name']}'**\n"\
                f"{information['gmaps_loc']}"

            await message.author.send(response_msg)
        else:
            response_msg = f'{user_name}, no sé en que edificio está salón. :('
            await message.author.send(response_msg)
    elif sections[0] == '!salon':
        response_msg = f'No me especificaste cual salon quieres que busque.\nIntenta en este formato: !salon:*<codigo>*\n'\
            'Si el salon contiene letras (ej: Fisica B) escribelo con guión. -> *!salon:F-B*'
        await message.author.send(response_msg)
