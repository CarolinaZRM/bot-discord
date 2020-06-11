import asyncio
import os
from datetime import datetime

import better_profanity
import discord

import bot
import log
from event_handlers import (channel, counselor, fun_games, join,
                            prepa, sanitize, actions)

client = discord.Client()


async def task():
    log.debug(f'[INFO] [Time: {datetime.utcnow()}] Starting.')
    await client.wait_until_ready()
    log.debug(f'[INFO] [Time: {datetime.utcnow()}] Started.')
    while True:
        await asyncio.sleep(1)


def handle_exit():
    log.debug(f"[DEBUG] Handling")
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
        log.debug(f'[INFO] [Func: on_message] MessageObj: {message}')

        if (message.author.bot):
            # Events related to bot response
            return

        has_profanity = await sanitize.profanity_filter(message)
        if has_profanity:
            log.debug('[DEBGU Has profanity')
            return

        log.debug('[INFO] passed the filter')

        # Created event passed Message object to use for response of bot to discord client
        await fun_games.event_ping_pong(message)
        await fun_games.event_guessing_game(message, client)
        await actions.event_get_curriculum(message)
        await actions.event_telephone_guide(message)

        if bot.is_sender_admin(message):
            # commands for admins and student counselors
            log.debug('[DEBUG] Entered Counselor Auth Zone')
            await channel.event_user_count(message)
            await counselor.event_help_menu(message)
        elif bot.is_sender_prepa(message):
            # commands for prepas
            await prepa.event_help_menu(message)
            await message.channel.send("Prepa Requested Something")

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        has_profanity = await sanitize.profanity_filter(after)

    @client.event
    async def on_member_join(member: discord.Member):
        await join.event_welcome_member(client, member)

    @client.event
    async def on_member_update(before, after):
        if before.roles != after.roles:
            log.debug(f'[DEBUG] before: {before} After: {after}')
            bot.update_admin_list(client)

    @client.event
    async def on_ready():
        log.debug(f'[DEBUG] Guild Obj: {client.guilds}')
        bot.update_admin_list(client)
        log.debug('[VERBOSE] On Ready Finished.')

    client.loop.create_task(task())
    try:
        TOKEN = bot.readToken()
        client.loop.run_until_complete(client.start(TOKEN))
    except SystemExit as e:
        log.debug(f'[DEBUG] Error {e}')
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        log.debug("[DEBUG] Program ended")
        break

    log.debug("[DEBUG] Bot restarting")
    client = discord.Client(loop=client.loop)
