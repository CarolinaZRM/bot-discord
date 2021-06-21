'''
//
//  constants/paths.py
//  py-bot-uprm
//
//  Created by Gabriel Santiago on 06/20/2021.
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''
import enum
from os import path

# Basic Paths
ROOT_PATH = path.abspath(path.dirname(path.dirname(__file__)))
RESOURCES = path.join(ROOT_PATH, 'res')

# Other helpful paths
AUDIO = path.join(RESOURCES, 'audio')
IMAGES = path.join(RESOURCES, 'images')
TEXT_FILES = path.join(RESOURCES, 'textfiles')


class PREPAS(enum.auto):
    __prepas = path.join(RESOURCES, 'prepas')
    PREPA_LIST = path.join(__prepas, 'teams_prepa_list.csv')
