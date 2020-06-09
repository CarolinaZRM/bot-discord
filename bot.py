import discord
import os
import asyncio

client = discord.Client()
client_id_num = 718911269813485568
guild_id_num = 718624993470316554

CURRENT_DIR = os.path.dirname(__file__) 
TOKEN_FILE = 'token.txt'
ADMINS_FILE = 'counselors.txt'
VALIDATED_USERS = []
DEBUG = True

def log(msg):
    if DEBUG:
        print(msg)

def readToken():
    f = open(os.path.join(CURRENT_DIR, TOKEN_FILE), "r")
    lines = f.readlines()
    return lines[0].strip()

def extractAdmins():
    f = open(os.path.join(CURRENT_DIR, ADMINS_FILE), "w")
    guild = client.get_guild(guild_id_num)
    print(guild)
    for member in guild.members:
        for role in member.roles:
            if role.name == "@EstudianteOrientador":
                f.write(str(member) + '\n')

    f.close()


def validateAdmins():
    admins = []
    file = open(os.path.join(CURRENT_DIR, ADMINS_FILE),"r")
    for counselor in file:
         admins.append(counselor.rstrip())
    file.close()
    return admins


async def task():
    await client.wait_until_ready()
    while True:
        await asyncio.sleep(1)
        print('Running')


def handle_exit():
    print("Handling")
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass


while True:        
    @client.event
    async def on_message(message):
        print(message)
        print(message.content)

        user_message = message.content
        id = client.get_guild(guild_id_num)
        admin_channels = ["counselors","admins","general"]
        prepa_channels = ["general"]
        bad_words = ["cabron","cabrona","mamabicho","puta","puto","pendejo","pendeja","fuck","shit","motherfucker","bellaco","bellaca","wlb","bicho","cb","beber"]

        sanitized = user_message.replace(',', '').replace(' ', '').replace('-', '').lower()
        log(f'Sanitized String: {sanitized}')

        # Tu eres un MAMABI CHo
        for bad_word in bad_words:
            if bad_word in sanitized:
                log(f'Containes a bad word: {user_message}')
                author = message.author.nick
                await message.channel.purge(limit=1)
                print(f"""{author} said a bad word, deleting message""")
                await message.channel.send(f"""{author} said a bad word, deleting message""")

        log('passed the filter')  

        if "!" in message.content and str(message.channel) in admin_channels and str(message.author) in VALIDATED_USERS:  #commands for admins and student counselors
            #ADD if message.content == !COMMAND: to add new commands
            if message.content == "!users":
                await message.channel.send(f"""Number of Members: {id.member_count}""")

            if message.content == "!help":
                embed = discord.Embed(title="Bot Commands for Prepas",description="Useful commands for prepas to ask the bot")
                embed.add_field(name="/curriculo YOUR_DEPT", value="Gives the prepa the curriculum they request (INEL/ICOM/INSO/CIIC)")
                embed.add_field(name="/map", value="Gives the prepa a map of UPRM")
                embed.add_field(name="/links", value="Gives the prepa a PDF with all the important links of UPRM")
                embed.add_field(name="/emails", value="Gives prepa a PDF with some important emails they can use")
                embed.add_field(name="/office YOUR_DEPT", value="Tells the prepa what their dept office number is (INEL/ICOM or INSO/CIIC)")
                await message.author.send(content=None, embed=embed)

            log(message.content)
            if "!curriculo" in message.content.lower(): #Asked for curriculum
                split = message.content.split(" ")
                if len(split) == 1:
                    await message.channel.send("Tienes que decirme que curriculo quieres! (INEL/ICOM/INSO/CIIC)")
                else:
                    if split[1].upper() == "INEL":
                        await message.channel.send("Electrical Engineering Curriculum:")
                        await message.channel.send(file=discord.File("res/curriculos/INEL.pdf"))
                    if split[1].upper() == "ICOM":
                        await message.channel.send("Computer Engineering Curriculum:")
                        await message.channel.send(file=discord.File("res/curriculos/ICOM.pdf"))
                    if split[1].upper() == "INSO":
                        await message.channel.send("Software Engineering Curriculum:")
                        await message.channel.send(file=discord.File("res/curriculos/INSO.pdf"))
                    if split[1].upper() == "CIIC":
                        await message.channel.send("Computer Science & Engineering Curriculum:")
                        #await message.channel.send(file=discord.File("res/curriculos/CIIC.pdf")) for when CIIC curriculum is updated
                        await message.channel.send("https://www.uprm.edu/cse/bs-computer-science-and-engineering-2/")

        elif "/" in message.content and str(message.channel) in prepa_channels and str(message.author) not in VALIDATED_USERS:  #commands for prepas
            #ADD if /COMMAND in message.content: to add new commands
            if "/help" in message.content.lower():
                embed = discord.Embed(title="Bot Commands for Prepas",description="Useful commands for prepas to ask the bot")
                embed.add_field(name="/curriculo YOUR_DEPT",value="Gives the prepa the curriculum they request (INEL/ICOM/INSO/CIIC)")
                embed.add_field(name="/map",value="Gives the prepa a map of UPRM")
                embed.add_field(name="/links",value="Gives the prepa a PDF with all the important links of UPRM")
                embed.add_field(name="/emails", value="Gives prepa a PDF with some important emails they can use")
                embed.add_field(name="/office YOUR_DEPT", value="Tells the prepa what their dept office number is (INEL/ICOM or INSO/CIIC)")
                await message.channel.send(content=None, embed=embed)

            if "/curriculo" in message.content.lower(): #Asked for curriculum
                split = message.content.split(" ")
                if len(split) == 1:
                    await message.channel.send("Tienes que decirme que curriculo quieres! (INEL/ICOM/INSO/CIIC)")
                else:
                    if split[1].upper() == "INEL":
                        await message.channel.send("Electrical Engineering Curriculum:")
                        await message.channel.send(file=discord.File("res/curriculos/INEL.pdf"))
                    if split[1].upper() == "ICOM":
                        await message.channel.send("Computer Engineering Curriculum:")
                        await message.channel.send(file=discord.File("res/curriculos/ICOM.pdf"))
                    if split[1].upper() == "INSO":
                        await message.channel.send("Software Engineering Curriculum:")
                        await message.channel.send(file=discord.File("res/curriculos/INSO.pdf"))
                    if split[1].upper() == "CIIC":
                        await message.channel.send("Computer Science & Engineering Curriculum:")
                        # await message.channel.send(file=discord.File("res/curriculos/CIIC.pdf")) for when CIIC curriculum is updated
                        await message.channel.send("https://www.uprm.edu/cse/bs-computer-science-and-engineering-2/")

            print(f"""{message.author.nick} requested something""")
            await message.channel.send("Prepa Requested Something")


    @client.event
    async def on_member_join(member: discord.Member):
        #Greets you to server
        await member.send(f"""Welcome to URPM {member.name}!""")
        await member.send("Please give me your full name so we know who you are in the server!")

        def check(m):  # checks if message was sent by someone other than the bot
                return m.author != client.user

        #Extracts the name of the student from the DM
        name = await client.wait_for("message", check=check)
        #Replaces their old name to the one they provided in the DM to the bot
        print(f"""{name.author}'s nickname was changed to {name.content}""")
        await member.edit(nick=str(name.content))

    @client.event
    async def on_ready():
        print(client.guilds)
        extractAdmins()
        VALIDATED_USERS = validateAdmins()

    client.loop.create_task(task())
    try:
        TOKEN = readToken()
        client.loop.run_until_complete(client.start(TOKEN))
    except SystemExit:
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        print("Program ended")
        break

    print("Bot restarting")
    client = discord.Client(loop=client.loop)
