import discord
id_num = 718911269813485568

def readToken():
    f = open("token.txt", "r")
    lines = f.readlines()
    return lines[0].strip()

def validateAdmins():
    admins = []
    file = open("counselors","r")
    lines = file.readlines()
    for counselor in lines:
        admins.append(counselor)
    return admins

valid_users = validateAdmins()  # list with the counselors to mamage the server
token = readToken()
client = discord.Client()



@client.event
async def on_message(message):
    id = client.get_guild(id_num)
    channels = ["test"]
    if str(message.channel) in channels and str(message.author) in valid_users:  #commands for admins and student counselors
        if message.content == "!users":
            await message.channel.send(f"""Number of Members: {id.member_count}""")

    elif "/" in message.content and ("admin" not in message.author.roles or "studentCounselor" not in message.author.roles):  #commands for prepas
        print(f"""{message.author.nick} requested something""")
        await message.channel.send("Prepa Requested Something")

    else:  #Prepa tried and admin command
        if "!" in message.content:
            print(f"""User: {message.author.nick} tried to do command {message.content}, in channel {message.channel}""")
            await message.channel.send("No eres Made ni un Estudiante Orientador para realizar estos comandos")


@client.event
async def on_member_join(member: discord.Member):
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



client.run(token)


