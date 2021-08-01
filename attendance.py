import collections
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
        print('*' * 30)

        guild: discord.Guild = self.get_guild(config.GUILD_ID_NUM)
        channel = guild.get_channel(CHANNEL_ID)

        print('=> Obteniendo miembros conectados...')

        members_in_attendance = [(idx + 1, member.nick if member.nick else member.name, '|'.join(filter(lambda role: role != '@everyone', [role.name for role in member.roles])))
                                 for idx, member in enumerate(channel.members)]

        print('=> Lista de miembros descargada...')

        now = datetime.now()  # current date and time
        formatted_datetime = now.strftime('%Y%m%d%H%M%S')

        list_file_path = self.attendance_list(
            members_in_attendance, formatted_datetime)
        stats_file_path = self.attendance_stats(
            members_in_attendance, formatted_datetime)

        print()
        print(
            f'=> Lista de miembros en el canal "{channel}" fue exitosamente guardada en el archivo:')
        print(f'=> {path.abspath(list_file_path)}')

        print()
        print(
            f'=> Estadisticas de miembros en el canal "{channel}" fue exitosamente guardada en el archivo:')
        print(f'=> {path.abspath(stats_file_path)}')
        print('*' * 30)

    def attendance_list(self, members_in_attendance, formatted_datetime):
        file_name = f'attendance-{formatted_datetime}.csv'

        with open(file_name, 'w') as attendance_file:
            #  Create instance of CSV Writer
            wtr = csv.writer(attendance_file)

            # Create csv header
            wtr.writerow(['ID', 'Nickname/Account Username', 'Lista de roles'])

            #  Save members list to CSV
            for connected_member in members_in_attendance:
                wtr.writerow([str(i) for i in connected_member])

        return path.abspath(file_name)

    def attendance_stats(self, members_in_attendance, formatted_datetime):
        file_name = f'attendance-stats-{formatted_datetime}.csv'

        member_roles_count = collections.defaultdict(int)

        for member in members_in_attendance:
            # in position 3 of the members list is the roles list separated by "|"
            if len(member[2]) == 0:
                member_roles_count['No assigned yet'] += 1
                continue

            member_roles = member[2].split('|')

            for role in member_roles:
                member_roles_count[role] += 1

        # save into stats file
        with open(file_name, 'w') as stats_file:
            writer = csv.writer(stats_file)
            writer.writerow(
                ['ID', 'Role Name', 'Quantity of members with role'])
            for idx, item in enumerate(sorted(member_roles_count.items())):
                writer.writerow([idx + 1, item[0], item[1]])

        return path.abspath(file_name)


client = AssistanceClient(intents=enabled_intents)
client.run(config.BOT_TOKEN)
