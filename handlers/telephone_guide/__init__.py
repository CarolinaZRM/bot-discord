'''
//  /handlers/telephone_guide/__init__.py
//  py-bot-uprm
//
//  Created by Gabriel S. Santiago on 06/23/2021
//  Copyright © 2021 bermedDev. All rights reserved.
//  Copyright © 2021 agSant01. All rights reserved.
//  Copyright © 2021 teamMADE. All rights reserved.
'''

from .telephone_guide_help import get_guide_handler, get_telephone_guide_help, is_command

__all__ = [
    get_telephone_guide_help,
    get_guide_handler,
    is_command
]
