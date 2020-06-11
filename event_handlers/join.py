import discord
import log


async def greet_new_member(client: discord.Client, member: discord.Member):
    # Greets you to server
    # await member.send(f"""Welcome to URPM {member.name}!""")
    await member.send("Please give me your full name so we know who you are in the server!")

    # checks if message was sent by the user and in the DM
    def check_same_user(client_response):
        return client_response.author == client.user

    # Extracts the name of the student from the DM
    name = await client.wait_for("message", check=check_same_user)

    # Replaces their old name to the one they provided in the DM to the bot
    print(f"""{name.author}'s nickname was changed to {name.content}""")
    await member.edit(nick=str(name.content))
