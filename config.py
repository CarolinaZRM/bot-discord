# Used in HEROKU Environment
import os
import sys

# Used in development environment
from dotenv import dotenv_values as __dotenv_values

BOT_TOKEN = None
CLIENT_ID_NUM = None
GUILD_ID_NUM = None
LOG_LEVEL = None
LOG_FILE = None


def __init_config():
    current_module = sys.modules[__name__]

    # Get posible values from .env in root directory
    config_values = __dotenv_values()

    # If dict from dotenv is empty fallback to os.environ as default Environment Variable provider
    if len(config_values) == 0:
        config_values = os.environ

    print(f"| Env Variables: {config_values}")

    __required_variables = ("BOT_TOKEN", "CLIENT_ID_NUM", "GUILD_ID_NUM")

    # import config variables from the .env file at the root of the project
    for key, value in config_values.items():
        if len(value) == 0 and key in __required_variables:
            raise Exception(
                "Uninitialized value in .env file on the root of the project."
            )

        # set the attributes for the config object
        setattr(current_module, str(key), str(value) or None)

    # Env variables validation
    for value in __required_variables:
        if not hasattr(current_module, value):
            raise Exception("Missing required config Variable")


__init_config()
