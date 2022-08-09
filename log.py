"""
//
//  log.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.

"""
import logging
import config

if not config.LOG_LEVEL:
    config.LOG_LEVEL = "ERROR"


logging.basicConfig(
    level=logging.getLevelName(config.LOG_LEVEL),
    filename=config.LOG_FILE,
    format="%(asctime)s - [%(levelname)s][%(name)s] - %(message)s",
)


def info(msg) -> None:
    logging.info(msg)


def debug(msg) -> None:
    logging.debug(msg)


def error(msg) -> None:
    print(msg)
    logging.error(msg)
