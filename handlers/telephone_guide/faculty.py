'''
//  /handlers/telephone_guide/faculty.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import discord

_CSE_FACULTY = {
    "Bienvenido Velez Rivera": "Acting Dean of Engineering\nFull Time Professor\nbienvenido.velez@upr.edu",
    "Pedro I. Rivera Vega": "Acting CSE Director\nFull Time Professor\np.rivera@upr.edu",
    "Manuel Rodriguez Martinez": "Associate Director\nFull Time Professor\nmanuel.rodriguez7@upr.edu",
    "Wilson Rivera Gallego": "Full Time Professor\nwilson.riveragallego@upr.edu",
    "Kejie Lu": "Full Time Professor\nkejie.lu@upr.edu",
    "Heidy Sierra Gil": "Associate Professor\nheidy.sierra1@upr.edu",
    "Emmanuel Arzuaga Cruz": "Full Time Professor\nearzuaga@ece.uprm.edu",
    "Marko Schütz Schmuck": "Full Time Professor\nmarko.schutz@upr.edu",
    "Jose L. Melendez": "Special Assistant to the Chancellor\nFull Time Professor\njose.melendez37@upr.edu",
    "Jaime Seguel": "Retired\njaime.seguel@upr.edu",
    "Juan O. Lopez Gerena": "Instructor\njuano.lopez@upr.edu"
}

_ECE_FACULTY = {
    "Gerson Beauchamp": "Full Time Professor\ngerson.beauchamp@upr.edu",
    "Jaime Arbona Fazzi": "Full Time Professor\njaime.arbona@upr.edu",
    "Jose Cedeño": "AFull Time Professor\njose.cedeno3@upr.edu",
    "Isidoro Couvertier": "Full Time Professor\nisidoro.couvertiero@upr.edu",
    "Shawn David Hunt": "Full Time Professor\nshawndavid.hunt@upr.edu",
    "Henrick Ierick": "Full Time Professor\nhenrick.ierick@upr.edu",
    "Rogelio Palomera ": "Full Time Professor\nrogelio.palomera@upr.edu",
    "Manuel Jimenez": "Full Time Professor\nmanuel.jimenez@upr.edu",
    "Nayda Santiago Santiago": "Full Time Professor\nnayda.santiago@upr.edu",
    "Hamed Parsiani Gobadi": "Full Time Professor\nhamed.parsiani@upr.edu",
    "Guillermo Serrano": "Full Time Professor\nguillermo.serrano.@upr.edu"
}


def get_faculty(sections):

    if len(sections) <= 1:
        return 'Por favor, especifica abreviación del departamento: INSO, ICOM, CIIC, INEL\n'\
            'Ejemplo: "!dept:inso"'

    department_name: str = sections[1].lower()
    embed = None
    if department_name in ('inso', 'ciic'):
        embed = discord.Embed(title="Facultad CSE",
                              description="")
        embed.add_field(name="Para más contacos de Facultad",
                        value="https://www.uprm.edu/cse/faculty/")
        for name, role in _CSE_FACULTY.items():
            embed.add_field(name=name, value=role)

    elif department_name in ('inel', 'icom'):
        embed = discord.Embed(title="Facultad ECE",
                              description="")

        embed.add_field(name="Para más contacos de Facultad",
                        value="https://ece.uprm.edu/people/faculty/#cn-top")
        for name, role in _ECE_FACULTY.items():
            embed.add_field(name=name, value=role)

    else:
        embed = "No reconozco ese departamento :eyes: :confused:\n"\
            "Intenta con: INEL, ICOM, INSO o CIIC"
    return embed
