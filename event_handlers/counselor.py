import discord
import log


async def event_help_menu(message: discord.Message):
    log.debug('[DEBUG] Enter Counselor Help')
    user_message = message.content

    if "!help" == user_message.lower():
        embed = discord.Embed(title="Bot Commands for Counselors",
                              description="Useful commands for counselors to ask the bot")
        embed.add_field(name="!curriculo YOUR_DEPT",
                        value="Gives the user the curriculum they request (INEL/ICOM/INSO/CIIC)")
        embed.add_field(
            name="!map", value="Gives the user a map of UPRM")
        embed.add_field(
            name="!links", value="Gives the user a PDF with all the important links of UPRM")
        embed.add_field(
            name="!emails", value="Gives user a PDF with some important emails they can use")
        embed.add_field(
            name="!office YOUR_DEPT", value="Tells the user what their dept office number is (INEL/ICOM or INSO/CIIC)")
        await message.author.send(content=None, embed=embed)
