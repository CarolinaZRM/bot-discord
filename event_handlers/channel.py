import discord, bot
from main import client


async def event_user_count(message : discord.Message):
    id = bot.GUILD_ID_NUM
    guild = client.get_guild(id)
    if "!user-count" == message.content.lower():

        await message.channel.send(f"""Number of Members: {guild.member_count}""")