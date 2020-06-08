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
async def on_member_update(before, after):
    nickname = after.nick
    if nickname:
        if nickname.lower().count("tim") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="Invalid Nickname Change")


@client.event
async def on_member_join(member: discord.Member):
    await member.send(f"""Welcome to the server {member.name}!""")
    await member.send("Please enter your full name: ")

    def check(m):  # checks if message was sent by someone other than the bot
            return m.author != client.user

    name = await client.wait_for("message",check=check)
    await member.edit(nick=str(name.content))


client.run(token)


