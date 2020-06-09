import discord
import os
import asyncio
from datetime import datetime
from event_handlers import fun_games

client = discord.Client()
client_id_num = 718911269813485568
guild_id_num = 718624993470316554

CURRENT_DIR = os.path.dirname(__file__) 
TOKEN_FILE = 'token.txt'
ADMINS_FILE = 'counselors.txt'
VALIDATED_USERS = []
DEBUG = True

### PDF Files
CURRICULO_INEL = os.path.join(CURRENT_DIR, "res","curriculos", "INEL.pdf")
CURRICULO_INSO = os.path.join(CURRENT_DIR, "res","curriculos", "INSO.pdf")
CURRICULO_CIIC = os.path.join(CURRENT_DIR, "res","curriculos", "CIIC.pdf")
CURRICULO_ICOM = os.path.join(CURRENT_DIR, "res","curriculos", "ICOM.pdf")
CURRICULO_CIIC_LINK = "https://www.uprm.edu/cse/bs-computer-science-and-engineering-2/"

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
    print(f'[INFO] [Time: {datetime.utcnow()}] Starting.')
    await client.wait_until_ready()
    print(f'[INFO] [Time: {datetime.utcnow()}] Started.')
    while True:
        await asyncio.sleep(1)


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
        # event_handlers.logic_for_event1(message)
        # event_handlers.logic_for_event2(message)
        # event_handlers.logic_for_event3(message)

        # Created event passed Message object to use for response of bot to discord client
        await fun_games.event_ping_pong(message)

        log(f'[INFO] [Func: on_message] MessageObj: {message}')

        if (message.author.bot):
            log(f'[DEBUG] Message from bot. Message: {message.content}')
            return

        user_message = message.content
        guild_id = client.get_guild(message.guild.id)
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

        log('[INFO] passed the filter')  
        
        #commands for admins and student counselors
        if str(message.channel).lower() in admin_channels and str(message.author) in VALIDATED_USERS:  
            log('[DEBUG] Entered Counselor Auth Zone')
            if  "!user-count" in user_message.lower():
                await message.channel.send(f"""Number of Members: {guild_id.member_count}""")

            if "!help" in user_message.lower():
                embed = discord.Embed(title="Bot Commands for Counselors",description="Useful commands for counselors to ask the bot")
                embed.add_field(name="!curriculo YOUR_DEPT", value="Gives the user the curriculum they request (INEL/ICOM/INSO/CIIC)")
                embed.add_field(name="!map", value="Gives the user a map of UPRM")
                embed.add_field(name="!links", value="Gives the user a PDF with all the important links of UPRM")
                embed.add_field(name="!emails", value="Gives user a PDF with some important emails they can use")
                embed.add_field(name="!office YOUR_DEPT", value="Tells the user what their dept office number is (INEL/ICOM or INSO/CIIC)")
                await message.author.send(content=None, embed=embed)

            if "!curriculo" in user_message.lower(): #Asked for curriculum
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

            await message.channel.send("Prepa Requested Something")
            print(f"""{message.author.nick} requested something""")


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
    async def on_member_update(before, after):
        if before.roles != after.roles:
            print(f'[DEBUG] before: {before} After: {after}')
            extractAdmins()
            print(f'[INFO] [Time: {datetime.utcnow()}] [Func: on_member_update] Updated Admin List.')
            global VALIDATED_USERS 
            VALIDATED_USERS = validateAdmins()
       
    @client.event
    async def on_ready():
        print(client.guilds)
        extractAdmins()
        
        print(f'[INFO] [Time: {datetime.utcnow()}] [Func: on_ready] Updated Admin List.')
        global VALIDATED_USERS 
        VALIDATED_USERS = validateAdmins()
        log(f'[DEBUG] [Func: on_ready] {VALIDATED_USERS}')

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
