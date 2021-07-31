from os import path
from datetime import datetime
import discord
import csv
import config

# Enable intents.
# Documentation: https://discordpy.readthedocs.io/en/latest/intents.html
enabled_intents: discord.Intents = discord.Intents.default()

enabled_intents.members = True
enabled_intents.guilds = True

###
# The Channel ID to get attendance on.
#  - CHANGE IF NECESSARY
#  - CURRENTLY POITING TO: prepas_conferenceRoom
###
CHANNEL_ID = 849684994641494053


class AssistanceClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        guild: discord.Guild = self.get_guild(config.GUILD_ID_NUM)
        channel = guild.get_channel(CHANNEL_ID)

        print('=> Obteniendo miembros conectados...')

        members_in_attendance = [(idx + 1, member.nick if member.nick else member.name, '|'.join(filter(lambda role: role != '@everyone', [role.name for role in member.roles])))
                                 for idx, member in enumerate(channel.members)]

        print('=> Lista de miembros descargada...')

        now = datetime.now()  # current date and time
        formatted_datetime = now.strftime('%Y%m%d%H%M%S')

        file_name = f'attendance-{formatted_datetime}.csv'

        # Open File to write
        with open(file_name, 'w') as attendance_file:
            #  Create instance of CSV Writer
            wtr = csv.writer(attendance_file)

            # Create csv header
            wtr.writerow(['ID', 'Nickname/Account Username', 'Lista de roles'])

            #  Save members list to CSV
            for connected_member in members_in_attendance:
                wtr.writerow([str(i) for i in connected_member])

        print(
            f'=> Lista de miembros en el canal "{channel}" fue exitosamente guardada en el archivo:')
        print(f'=> {path.abspath(file_name)}')


client = AssistanceClient(intents=enabled_intents)
client.run(config.BOT_TOKEN)
