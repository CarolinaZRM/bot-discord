"""
//  /bot-discord/constants/paths.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/12
//
//  Last Modified: Friday, 12th August 2022 11:29:26 am
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
import enum
from os import path

# Basic Paths
ROOT_PATH = path.abspath(path.dirname(path.dirname(__file__)))
RESOURCES = path.join(ROOT_PATH, "res")

# Other helpful paths
AUDIO = path.join(RESOURCES, "audio")
CURRICULOS = path.join(RESOURCES, "curriculos")
EMBEDS = path.join(RESOURCES, "embeds")
IMAGES = path.join(RESOURCES, "images")
PROJECTS = path.join(RESOURCES, "proyectos")
TEXT_FILES = path.join(RESOURCES, "textfiles")


class PREPAS(enum.auto):
    __prepas = path.join(RESOURCES, "prepas")
    PREPA_LIST = path.join(__prepas, "teams_prepa_list.csv")
