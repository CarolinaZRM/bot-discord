# USed in development environment
from dotenv import dotenv_values
# Used in HEROKU Environment
import os

# Get posible values from .env in root directory
__config_values = dotenv_values()

# If dict from dotenv is empty fallback to os.environ as default Environment Variable provider
if len(__config_values) == 0:
    __config_values = os.environ

print(f'[DEBUG] | Env Variables: {__config_values}')

BOT_TOKEN = __config_values['BOT_TOKEN']

CLIENT_ID_NUM = int(__config_values['CLIENT_ID_NUM'])

GUILD_ID_NUM = int(__config_values['GUILD_ID_NUM'])

__required_variables = [
    BOT_TOKEN,
    CLIENT_ID_NUM,
    GUILD_ID_NUM
]

# Env variables validation
for value in __required_variables:
    if value is None or len(str(value)) == 0:
        raise Exception(
            'Uninitialized value in .env file on the root of the project.')
