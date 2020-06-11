import discord
import log


async def get_curriculum(message: discord.Message):
    user_message = message.content
    if "!curriculo" in user_message.lower():  # Asked for curriculum
        split = user_message.split(" ")
        if len(split) == 1:
            await message.channel.send("Tienes que decirme que curriculo quieres! (INEL/ICOM/INSO/CIIC)")
        else:
            if split[1].upper() == "INEL":
                await message.channel.send("Electrical Engineering Curriculum:")
                await message.channel.send(file=discord.File(CURRICULO_INEL))
            if split[1].upper() == "ICOM":
                await message.channel.send("Computer Engineering Curriculum:")
                await message.channel.send(file=discord.File(CURRICULO_ICOM))
            if split[1].upper() == "INSO":
                await message.channel.send("Software Engineering Curriculum:")
                await message.channel.send(file=discord.File(CURRICULO_INSO))
            if split[1].upper() == "CIIC":
                await message.channel.send("Computer Science & Engineering Curriculum:")
                # for when CIIC curriculum is updated
                # await message.channel.send(file=discord.File(CURRICULO_CIIC))
                await message.channel.send(CURRICULO_CIIC_LINK)
