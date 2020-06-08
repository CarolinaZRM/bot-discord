import discord, time, asyncio
id_num = 718911269813485568
messages = joined = 0


def readToken():
    f = open("token.txt", "r")
    lines = f.readlines()
    return lines[0].strip()

def validateAdmins():
    admins = []
    file = open("counselors.txt","r")
    for counselor in file:
        admins.append(counselor.rstrip())
    return admins

valid_users = validateAdmins()  # list with the counselors to manage the server
token = readToken()
client = discord.Client()

async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed(): #while bot is running
        try:
           with open("stats.txt","a") as stats:
               stats.write(f"""Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n""")
           messages = 0
           joined = 0

           await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)


@client.event
async def on_message(message):
    global messages, valid_users
    messages += 1
    id = client.get_guild(id_num)
    channels = ["test","general"]
    bad_words = ["cabron","cabrona","mamabicho","puta","puto","pendejo","pendeja","fuck","shit","motherfucker","bellaco","bellaca","wlb","bicho","cb"]


    for word in bad_words: #If someone says a profanity, remove it and expose who it was
        if word in message.content.lower():
            author = message.author.nick
            await message.channel.purge(limit=1)
            print(f"""{author} said a bad word, deleting message""")
            await message.channel.send(f"""{author} said a bad word, deleting message""")

    if str(message.channel) in channels and str(message.author) in valid_users:  #commands for admins and student counselors
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


    elif "/" in message.content and str(message.author) not in valid_users:  #commands for prepas
        #ADD if /COMMAND in message.content: to add new commands
        if "/help" in message.content:
            embed = discord.Embed(title="Bot Commands for Prepas",description="Useful commands for prepas to ask the bot")
            embed.add_field(name="/curriculo YOUR_DEPT",value="Gives the prepa the curriculum they request (INEL/ICOM/INSO/CIIC)")
            embed.add_field(name="/map",value="Gives the prepa a map of UPRM")
            embed.add_field(name="/links",value="Gives the prepa a PDF with all the important links of UPRM")
            embed.add_field(name="/emails", value="Gives prepa a PDF with some important emails they can use")
            embed.add_field(name="/office YOUR_DEPT", value="Tells the prepa what their dept office number is (INEL/ICOM or INSO/CIIC)")
            await message.channel.send(content=None, embed=embed)
        print(f"""{message.author.nick} requested something""")
        await message.channel.send("Prepa Requested Something")

    else:  #Prepa tried and admin command
        if "!" in message.content:
            print(f"""User: {message.author.nick} tried to do command {message.content}, in channel {message.channel}""")
            await message.channel.send("No eres Made ni un Estudiante Orientador para realizar estos comandos")



@client.event
async def on_member_join(member: discord.Member):
    global joined
    joined += 1
    #Greets you to server
    await member.send(f"""Welcome to URPM {member.name}!""")
    await member.send("Please give me your full name so we know who you are in the server!")

    def check(m):  # checks if message was sent by someone other than the bot
            return m.author != client.user

    #Extracts the name of the student from the DM
    name = await client.wait_for("message", check=check)
    #Replacses their old name to the one they provided in the DM to the bot
    print(f"""{name.author}'s nickname was changed to {name.content}""")
    await member.edit(nick=str(name.content))

client.loop.create_task(update_stats())
client.run(token)


