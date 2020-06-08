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
    if str(message.channel) in channels and str(message.author) in valid_users:
        # if message.content.find("!ping") != -1: TEST COMMAND
        #     await message.channel.send("pong!")
        if message.content == "!users":
            await message.channel.send(f"""Number of Members: {id.member_count}""")
    else:
        print(f"""User: {message.author} tired to do command {message.content}, in channel {message.channel}""")

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome to he server {member.mention}!""")
client.run(token)



