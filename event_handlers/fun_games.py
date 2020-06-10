import random

async def event_ping_pong(message):
    print('hi im ping pong')
    if message.content == 'ping':
        await message.channel.send('Pong :)')

async def event_guessing_game(message, client):
    def convert_to_int(value):
        try:
            return int(value)
        except Exception as _:
            return False

    response = None

    user_name = message.author.nick 
    
    if user_name is None:
        user_name = message.author.name

    if message.content == "?guess":
        await message.channel.send("I have a number from 1-100, can you guess it?\nYou can only type integers, or if you give up type 'GiveUp'")
        correct_answer = random.randint(1,101)
        
        while convert_to_int(response) != correct_answer:
            response = await client.wait_for("message", check=lambda response_message : response_message.author == message.author)
            response = response.content
            
            if  response.isdigit() and (convert_to_int(response) > 100 or convert_to_int(response) < 0):
                await message.channel.send(f"""Heyyy?? That is not between 0 and 100 Hahaha\nTry again {user_name}! :)""")
                continue
            elif response.isdigit() and convert_to_int(response) > correct_answer:
                await message.channel.send(f"""Guess a bit lower {user_name}!""")
                continue
            elif response.isdigit() and convert_to_int(response) < correct_answer:
                await message.channel.send(f"""Guess a bit higher {user_name}!""")
                continue
            
            elif response == "GiveUp":
                break

        if response != "GiveUp":
            await message.channel.send(f"""You win {user_name}! Congrats !""")
        else:
            await message.channel.send(f"""Gave up so soon {user_name}? The correct answer was {correct_answer}""")





