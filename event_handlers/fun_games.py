import random
from bot import client
def check(m):
    return m.author != client.user

async def event_ping_pong(message):
    print('hi im ping pong')
    if message.content == 'ping':
        await message.channel.send('Pong :)')

async def event_guessing_game(message):
    response = ""
    if message.content == "?guess":
        await message.channel.send("I have a number from 1-100, can you guess it? \n You can only type integers, or if you give up type 'give_up'")
        correct_answer = random.randint(1,101)

        while int(response) != correct_answer:
            response = await client.wait_for("message", check=check)

            if int(response) > correct_answer:
                await message.channel.send(f"""Guess a bit lower {message.author}!""")
                continue
            if int(response) < correct_answer:
                await message.channel.send(f"""Guess a bit higher {message.author}!""")
                continue
            if response == "give_up":
                break
        if response != "give_up":
            await message.channel.send(f"""You win {message.author.nick}! Congrats !""")
        else:
            await message.channel.send(f"""Gave up so soon {message.author}? The correct answer was {correct_answer}""")





