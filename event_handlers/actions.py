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
import csv
import os

import bot
import discord
import log
from handlers import building_parser, help_menu, telephone_guide
from constants import paths

# files
_RULE_FILE = os.path.join(paths.TEXT_FILES, "rules.txt")
_FAQ_FILE = os.path.join(paths.TEXT_FILES, "faq.csv")
_GOOGLE_ADD_CALENDAR = os.path.join(paths.IMAGES, "google_add_calendar.png")

# PDF Files
CURRICULO_INEL = os.path.join(paths.CURRICULOS, "INEL.pdf")
CURRICULO_INSO = os.path.join(paths.CURRICULOS, "INSO.pdf")
CURRICULO_CIIC = os.path.join(paths.CURRICULOS, "CIIC.pdf")
CURRICULO_ICOM = os.path.join(paths.CURRICULOS, "ICOM.pdf")


async def event_get_calendar(message: discord.Message):
    user_message = message.content

    user_name = None

    if hasattr(message.author, 'nick'):
        user_name = message.author.nick
    else:
        user_name = message.author.name

    if "!calendario" == user_message:
        await message.author.send(
            f"Hola {user_name}! Aquí adjunto el calendario académico de UPRM.\n"
            "**Calendario Académico:** https://www.uprm.edu/decestu/calendario/"
        )
        await message.author.send("También puedes anadir este calendario a tu calendario personal.\n"
                                  "Presta atencion a la esquina inferior derecha del calendario.\nSe ve asi:")
        await message.author.send(file=discord.File(_GOOGLE_ADD_CALENDAR))


async def get_org_info(message: discord.Message):
    log.debug('[DEBUG] Entered Student Org')
    user_message = message.content
    if "!ls_student_orgs:ORG" == user_message:
        await message.author.send("Puede que te hayas confundido :sweat_smile:\n"
                                  "'Org' = Organización\n"
                                  "Intenta usar el comando ```!ls_student_orgs:ORG``` sustituyendo ORG con una de las siguientes abreviaciones:\n"
                                  "IEEE/EMC/HKN/RAS_CSS/COMP_SOC/CAS/PES/WIE/ACM_CSE/CAHSI/SHPE")
    if "!ls_student_orgs" in user_message.lower():
        split = user_message.split(":")
        if len(split) == 1:
            await message.author.send("No me dijiste que organización; no está en lista.\n"
                                      "Intenta con: IEEE/EMC/HKN/RAS_CSS/COMP_SOC/CAS/PES/WIE/ACM_CSE/CAHSI/SHPE")
        else:
            if split[1].upper() == "EMC":
                await message.author.send("Here's information on IEEE Electromagnetics Council:\n")
                await message.author.send("Electromagnetics Council (EMC) is a joint chapter founded in 2012 under the IEEE UPRM Branch. It is to be recognized\n"
                                          "as a potential tool for the enhancement in the development of our students as future professionals in RF disciplines.\n"
                                          "It is our best interest to spread knowledge and increase awareness in this area of study to students from the campus that\n"
                                          "are or might be interested in subjects related to applications in applied electromagnetics. By professional and technical\n"
                                          "development activities we wish to help students reach their leadership and technical potentials.\n")
                await message.author.send("Facebook Page: https://www.facebook.com/emc.uprm\n"
                                          "Website: http://emc.uprm.edu")

            if split[1].upper() == "IEEE":
                await message.author.send("Here's information on IEEE:\n")
                await message.author.send("IEEE’s core purpose is to develop industry leaders in professional and technical expertise for them to\n"
                                          "contribute in our community and society.\n IEEE-UPRM chapter’s mission is to provide its members with the highest and most competitive knowledge\n"
                                          "in diverse areas of engineering in order for them to expand their abilities consistent with industry needs.\n")
                await message.author.send("Email: ieee@uprm.edu\n"
                                          "Facebook & Twitter: ieeeuprm")
            if split[1].upper() == "HKN":
                await message.author.send("Here's information on Eta Kappa Nu:\n")
                await message.author.send("They are the UPRM Eta Kappa Nu chapter called Lambda Tau. They are dedicated to encourage and recognize outstanding\n"
                                          "students in the fields of Science, Technology, Engineering, and Mathematics (STEM) within the UPR’s Mayaguez Campus.\n"
                                          "Candidates and members that have shown professional achievements and academic excellence will have the chance to form\n"
                                          "part of a dynamic environment dedicated to help them succeed in all aspects of their personal and professional activities.\n")
                await message.author.send("Email: hkn.uprm@gmail.com\n"
                                          "Facebook Page: https://www.facebook.com/IEEE.HKN/\n"
                                          "Instagram: @hkn_lambdatau")
            if split[1].upper() == "RAS_CSS":
                await message.author.send("Here's IEEE Robotics and Automation Society & Control Systems Society\n")
                await message.author.send("El joint chapter de la Robotics and Automation Society & Control and Systems Society tienen como misión educar a la comunidad,\n"
                                          "tanto universitario como la no universitaria, acerca de la robótica, automatización de procesos y los sistemas de control. Esto\n"
                                          "lo llevamos a cabo mediante nuestros proyectos y talleres que ofrecemos tanto a los estudiantes de la universidad como a estudiante\n"
                                          "de escuela superior e intermedia a los cuales le llevamos talleres durante el año escolar.\n")
                await message.author.send("Emails: ras@uprm.edu; css@uprm.edu\n"
                                          "Facebook page: https://www.facebook.com/RAS.UPRM/\n"
                                          "Twitter: @ras_uprm")
            if split[1].upper() == "COMP_SOC":
                await message.author.send("Here's information on IEEE Computer Society:\n")
                await message.author.send("IEEE Computer Society is an IEEE technical branch dedicated to computing fields. It's a Hub for students interested in computing fields\n"
                                          "to network and learn, and is a Link between students and companies. Their mission and vision is to be the leading provider of technical\n"
                                          "information, community services, and personalized services to the world's computer professionals, and to be universally recognized for the\n"
                                          "contributions in various areas.\n")
                await message.author.send("Website: https://academic.uprm.edu/computersociety/\n"
                                          "Email: computersociety@uprm.edu\n"
                                          "Twitter: @SocietyIeee"
                                          "Facebook Page: https://www.facebook.com/computersociety.uprm/")
            if split[1].upper() == "CAS":
                await message.author.send("Here's information on IEEE Circuits And Systems Society:\n")
                await message.author.send("At the IEEE Circuits and System, we do not focus only in developing brighter students; we provide them with the necessary tools and experience\n"
                                          "to help them grow into future professionals and responsible leaders.  This we achieve through our seminars, technical sessions, distinguished\n"
                                          "lecturers, workshops, and by promoting the participation of the students on the society’s board.\n")
                await message.author.send("Email: cas@uprm.edu\n"
                                          "Facebook Page: https://www.facebook.com/cas.uprm/\n"
                                          "Website: http://cas.uprm.edu/")
            if split[1].upper() == "PES":
                await message.author.send("Here's IEEE Power & Energy Society")
                await message.author.send("PES is the leading provider of scientific information on electric power and energy for the betterment of society and the preferred professional\n"
                                          "development source for our members.")
                await message.author.send("Email: pes.upr@gmail.com\n"
                                          "Website: http://ece.uprm.edu/pes/\n"
                                          "Facebook Page: https://www.facebook.com/ieepesuprm/\n")
            if split[1].upper() == "WIE":
                await message.author.send("Here's information on IEEE Women in Engineering:\n")
                await message.author.send("IEEE-Women in Engineering is an organization dedicated to promote women engineers and scientists.\n"
                                          "Our goal is to encourage the growth of women pursuing degrees in engineering fields where they are \n"
                                          "strongly underrepresented. As a student organization, we support students who have already chosen an\n"
                                          "engineering career to continue on their path by offering workshops and orientations, which will help\n"
                                          "them grow academically and professionally. We also try to promote careers in engineering for high school\n"
                                          "level students by offering outreach activities such as the STAR Program and the Engineering Workshop, which\n"
                                          "aim to teach them the benefits of pursuing a career in engineering.")
                await message.author.send("Web page: http://wie.uprm.edu\n"
                                          "Facebook page: facebook.com/wie.uprm\n"
                                          "Contact: wie@uprm.edu\n"
                                          "Phone: (787) 265-5402")
            if split[1].upper() == "ACM_CSE":
                await message.author.send("Here's information on Association for Computing Machinery:\n")
                await message.author.send("The ACM seeks to create an environment of convergence, offering quality and challenging learning experience,\n"
                                          "technical and professional enrichment that contribute to the individual development of each of our members. At\n"
                                          "the same time provide an excellent service focused on assisting all curricular and extracurricular needs for the\n"
                                          "course of his career to be one rewarding experience.")
                await message.author.send("Facebook page: https://www.facebook.com/ACM.ECE?fref=ts\n"
                                          "Contact: acm.students@ece.uprm.edu")
            if split[1].upper() == "CAHSI":
                await message.author.send("Here's information on Computing Alliance of Hispanic-Serving Institution:\n")
                await message.author.send("The Student Branch of the Computer Alliance of Hispanics Serving Institutions was established in 2006 to address the\n"
                                          "low representation of Hispanics in computing in both higher education and the workforce. CAHSI sets forth a flexible\n"
                                          "process using the conditions of collective impact that furthers the interchange of knowledge creation, adaptation,\n"
                                          "dissemination, and assessment. Goals include to increase the number of Hispanic students who enter the professorate in\n"
                                          "computing areas, or enter the computing workforce with advanced degrees, etc.")
                await message.author.send("Facebook: @uprm.cahsi\n"
                                          "Twitter: @cahsi_uprm\n"
                                          "Instagram: @cahsi_uprm")
            if split[1].upper() == "SHPE":
                await message.author.send("Here's some information on Society of Hispanic Professional Engineers:\n")
                await message.author.send("SHPE is the nation's largest association dedicated to fostering Hispanic leadership in the STEM field. SHPE offers all Junior,\n"
                                          "undergraduate, graduate, and professional members the necessary resources to promote SHPE’s mission to realize its fullest potential\n"
                                          "and to impact the world through STEM awareness, access, support and development. Their objective was to form a national organization of\n"
                                          "professional engineers to serve as role models in the Hispanic community.")
                await message.author.send("Website: http://shpe.uprm.edu/\n"
                                          "Facebook Page: https://www.facebook.com/SHPEUPRM/")



async def get_prj_info(message: discord.Message):
    log.debug('[DEBUG] Entered Project')
    user_message = message.content
    if "!ls_projects" in user_message.lower():
        split = user_message.split(":")
        if len(split) == 1:
            await message.author.send("No me dijiste que projecto; no está en lista.\n Intenta con: A, B, C")
        else:
            if split[1].upper() == "EMC":
                await message.author.send("Here's EMC")
            if split[1].upper() == "IEEE":
                await message.author.send("Here's IEEE")


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


async def event_telephone_guide(message: discord.Message):
    log.debug('[DEBUG] Entered telephone guide')
    client_message: str = message.content
    sections = client_message.split(':')

    if telephone_guide.is_command(sections):
        function_call = telephone_guide.get_guide_handler(sections)
        if function_call:
            response = function_call(sections)
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
            await message.channel.send('No entendí el código de ese salon.\nIntenta escribirlo con guión.')
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
        response_msg = 'No me especificaste cual salon quieres buscar.\nIntenta en este formato: !salon:*<código>*\n'\
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


async def generate_server_rules(message: discord.Message):
    log.debug("[RULE-DBG] Entered Rule Generator")
    log.debug(
        f"""[RULE-DBG] Command Requested was {message.content.lower()}""")
    if message.content.lower() == "!reglas":
        embed = discord.Embed(title="Reglas del Servidor de Discord Oficial de Team MADE",
                              description="Aquí están todas las reglas a seguir en el servidor en esta semana de orientación virtual 2020")
        rules = open(_RULE_FILE, "r")
        ruleCount = 1
        for rule in rules:
            embed.add_field(name=f"""Regla {ruleCount}""", value=rule)
            ruleCount += 1
        await message.channel.send(content=None, embed=embed)


async def generate_faq(message: discord.Message):
    if message.content == "!faq":
        embed = discord.Embed(title="Frequently Asked Questions",
                              description="Aquí puedes encontrar ciertas preguntas que pueden surgir durante la semana")
        with open(_FAQ_FILE) as faq_file:
            rows = csv.DictReader(faq_file, delimiter=',')
            for row in rows:
                question = dict(row)
                embed.add_field(
                    name=f"{question['num']}) {question['question']}", value=question['answer'])

        await message.channel.send(content=None, embed=embed)
