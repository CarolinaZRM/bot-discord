"""
//
//  actions.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
import discord
import log
import os
import csv
from handlers import telephone_guide, building_parser, help_menu
from typing import Dict
import bot

# go up two dirs
# at bot-discord/
CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))


_RULE_FILE = os.path.join(CURRENT_DIR, "res", "textfiles","rules.txt")
# PDF Files
CURRICULO_INEL = os.path.join(CURRENT_DIR, "res", "curriculos", "INEL.pdf")
CURRICULO_INSO = os.path.join(CURRENT_DIR, "res", "curriculos", "INSO.pdf")
CURRICULO_CIIC = os.path.join(CURRENT_DIR, "res", "curriculos", "CIIC.pdf")
CURRICULO_ICOM = os.path.join(CURRENT_DIR, "res", "curriculos", "ICOM.pdf")
CURRICULO_CIIC_LINK = "https://www.uprm.edu/cse/bs-computer-science-and-engineering-2/"

_FAQ_FILE = os.path.join(
    CURRENT_DIR, "res", "textfiles", "faq.csv")

_GOOGLE_ADD_CALENDAR = os.path.join(
    CURRENT_DIR, "res", "images", "google_add_calendar.png")


async def event_get_calendar(message: discord.Message):
    user_message = message.content

    user_name = None

    if hasattr(message.author, 'nick'):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    if "!calendario" == user_message:
        await message.author.send(
            f"Hola {user_name}! Aqui adjunto el calendario academico de UPRM.\n"
            "**Calendario Academico:** https://www.uprm.edu/decestu/calendario/"
        )
        await message.author.send("Tambien puedes anadir este calendario a tu calendario personal.\n"
                                  "Presta atencion a la esquina inferior derecha del calendario.\nSe ve asi:")
        await message.author.send(file=discord.File(_GOOGLE_ADD_CALENDAR))


async def event_get_curriculum(message: discord.Message):
    log.debug('[DEBUG] Entered Curriculum')
    user_message = message.content
    if "!curriculo" in user_message.lower():  # Asked for curriculum
        split = user_message.split(":")
        log.debug('[DEBUG] Contains Curriculum')
        if len(split) == 1:
            await message.author.send("No me dijiste que curriculo necesitas :slight_frown:\nIntenta con: INEL/ICOM/INSO/CIIC")
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
                await message.author.send(file=discord.File(CURRICULO_CIIC))
                # await message.author.send(CURRICULO_CIIC_LINK)


async def event_telephone_guide(message: discord.Message):
    log.debug('[DEBUG] Entered telephone guide')
    client_message: str = message.content
    sections = client_message.split(':')

    if telephone_guide.is_command(sections):
        function_call = telephone_guide.get_guide_handler(sections)
        if function_call:
            # reponse = embed
            response = function_call(sections)
            # message.author.send(embed)
            if isinstance(response, str):
                await message.author.send(response)
            elif isinstance(response, discord.Embed):
                await message.author.send(content=None, embed=response)
            elif isinstance(response, dict):
                if 'content_first' in response:
                    await message.author.send(content=response['content_first'])
                    await message.author.send(content=None, embed=response['embed'])
                    return
                if 'embed' in response:
                    await message.author.send(content=None, embed=response['embed'])
                if 'content' in response:
                    await message.author.send(content=response['content'])


async def event_parse_university_building(message: discord.Message):
    client_message: str = message.content
    sections = client_message.split(':')

    user_name = None

    if hasattr(message.author, 'nick'):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    # response = f'Hola {user_name}, Es posible que este salon se encuentre en el edificio:\n'
    if len(sections) > 1 and sections[0] == '!salon' and len(sections[1]) > 0:

        if not building_parser.is_valid_room_number(sections):
            await message.channel.send('No entendi el codiog de ese salon.\nIntenta escribirlo con guión.')
            return

        information = building_parser.get_building_information(sections)

        if information:
            response_msg = f"Hola {user_name}! Es posible que este salon se encuentre en el edificio: **'{information['name']}'**\n"\
                f"{information['gmaps_loc']}"

            await message.channel.send(response_msg)
        else:
            response_msg = f'{user_name}, no sé en que edificio está salón. :('
            await message.channel.send(response_msg)
    elif sections[0] == '!salon':
        response_msg = f'No me especificaste cual salon quieres buscar.\nIntenta en este formato: !salon:*<codigo>*\n'\
            'Si el salon contiene letras (ej: Fisica B) escribelo con guión. -> *!salon:F-B*'
        await message.channel.send(response_msg)


async def event_help_menu(message: discord.Message):
    if message.content.lower() == '!help':
        msg_author: discord.User = message.author
        if bot.is_sender_counselor(message):
            help_menu_embed = help_menu.help_menu_for_counselor()
        elif bot.is_sender_prepa(message):
            help_menu_embed = help_menu.help_menu_for_prepa()
        else:
            help_menu_embed = help_menu.help_menu_base()
        await msg_author.send(content=None, embed=help_menu_embed)


async def generate_server_rules(message : discord.Message):
    log.debug("[RULE-DBG] Entered Rule Generator")
    log.debug(f"""[RULE-DBG] Command Requested was {message.content.lower()}""")
    if message.content.lower() == "!reglas":
        embed = discord.Embed(title="Reglas del Servidor de Discord Oficial de Team MADE",
                              description="Aquí estan todas las reglas a seguir en el servidor en esta semana de orientación virtual 2020")
        rules = open(_RULE_FILE,"r")
        ruleCount = 1
        for rule in rules:
            embed.add_field(name=f"""Regla {ruleCount}""", value=rule)
            ruleCount += 1
        await message.channel.send(content=None, embed=embed)

async def generate_faq(message : discord.Message):
    if message.content == "!faq":
        embed = discord.Embed(title= "Frequently Asked Questions", description="Aqui puedes encontrar ciertas preguntas que pueden surgirte durante la semana")
        with open(_FAQ_FILE) as faq_file:
            rows = csv.DictReader(faq_file,  delimiter=',')
            for row in rows:
                question = dict(row)
                embed.add_field(name=f"{question['num']}) {question['question']}", value=question['answer'])

        await message.channel.send(content=None, embed=embed)



