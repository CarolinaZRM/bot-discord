import discord
import os
import asyncio
import better_profanity
from datetime import datetime
from event_handlers import channel, fun_games, counselor, actions, sanitize, prepa, join

import log
import bot

client = discord.Client()

CURRENT_DIR = os.path.dirname(__file__)
TOKEN_FILE = os.path.join(CURRENT_DIR, "res", "textfiles", 'token.txt')

# PDF Files
CURRICULO_INEL = os.path.join(CURRENT_DIR, "res", "curriculos", "INEL.pdf")
CURRICULO_INSO = os.path.join(CURRENT_DIR, "res", "curriculos", "INSO.pdf")
CURRICULO_CIIC = os.path.join(CURRENT_DIR, "res", "curriculos", "CIIC.pdf")
CURRICULO_ICOM = os.path.join(CURRENT_DIR, "res", "curriculos", "ICOM.pdf")
CURRICULO_CIIC_LINK = "https://www.uprm.edu/cse/bs-computer-science-and-engineering-2/"


def readToken():
    f = open(os.path.join(CURRENT_DIR, TOKEN_FILE), "r")
    lines = f.readlines()
    return lines[0].strip()


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
            client.loop.run_until_complete(
                asyncio.wait_for(t, 5, loop=client.loop))
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
        log.debug(f'[INFO] [Func: on_message] MessageObj: {message}')

        if (message.author.bot):
            log.debug(f'[DEBUG] Message from bot. Message: {message.content}')
            return

        has_profanity = await sanitize.profanity_filter(message)

        if has_profanity:
            return

        log.debug('[INFO] passed the filter')

        # Created event passed Message object to use for response of bot to discord client
        await fun_games.event_ping_pong(message)
        await fun_games.event_guessing_game(message, client)
        await actions.get_curriculum(message)

        # Events related to bot response
        #

        # commands for admins and student counselors
        if bot.is_sender_admin(message):
            log.debug('[DEBUG] Entered Counselor Auth Zone')
            # command test
            await channel.event_user_count(message)
            await counselor.event_help_menu(message)

        # commands for prepas
        elif bot.is_sender_prepa(message):
            await prepa.event_help_menu(message)

            await message.channel.send("Prepa Requested Something")
            print(f"""{message.author.nick} requested something""")

    @client.event
    async def on_member_join(member: discord.Member):
        await join.event_welcome_member(client, member)

    @client.event
    async def on_member_update(before, after):
        if before.roles != after.roles:
            print(f'[DEBUG] before: {before} After: {after}')
            bot.update_admin_list(client)

    @client.event
    async def on_ready():
        print(client.guilds)
        bot.update_admin_list(client)
        log.debug('[VERBOSE] On Ready Finished.')

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
