from dotenv import dotenv_values

__config_values = dotenv_values()

BOT_TOKEN = __config_values['BOT_TOKEN']

CLIENT_ID_NUM = int(__config_values['CLIENT_ID_NUM'])

GUILD_ID_NUM = int(__config_values['GUILD_ID_NUM'])


# Env variables validation
for value in [BOT_TOKEN, CLIENT_ID_NUM, GUILD_ID_NUM]:
    if value is None or len(str(value)) == 0:
        raise Exception(
            'Uninitialized value in .env file on the root of the project.')
