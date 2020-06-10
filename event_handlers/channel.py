import discord


async def event_user_count(messsage: discord.Message):
    if "!user-count" == messsage.content.lower():
        await message.channel.send(f"""Number of Members: {guild_id.member_count}""")
