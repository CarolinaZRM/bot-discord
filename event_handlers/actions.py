import discord
import log
import os
from handlers import telephone_guide

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
            response = function_call(sections) #either an embed or str

            if isinstance(response, str):
                await message.author.send(response)
            else:
                await message.author.send(content=None, embed=response)
