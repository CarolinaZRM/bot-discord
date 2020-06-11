import discord
import log


async def event_help_menu(message: discord.Message):
    # ADD if /COMMAND in message.content: to add new commands
    if "/help" in message.content.lower():
        embed = discord.Embed(title="Bot Commands for Prepas",
                              description="Useful commands for prepas to ask the bot")
        embed.add_field(name="/curriculo YOUR_DEPT",
                        value="Gives the prepa the curriculum they request (INEL/ICOM/INSO/CIIC)")
        embed.add_field(
            name="/map", value="Gives the prepa a map of UPRM")
        embed.add_field(
            name="/links", value="Gives the prepa a PDF with all the important links of UPRM")
        embed.add_field(
            name="/emails", value="Gives prepa a PDF with some important emails they can use")
        embed.add_field(
            name="/office YOUR_DEPT", value="Tells the prepa what their dept office number is (INEL/ICOM or INSO/CIIC)")
        await message.channel.send(content=None, embed=embed)
