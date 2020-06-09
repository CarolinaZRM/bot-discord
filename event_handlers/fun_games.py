async def event_ping_pong(message):
    print('hi im ping pong')
    if message.content == 'ping':
        await message.channel.send('Pong :)')