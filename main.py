"""
//
//  main.py
//  py-bot-uprm
//
//  Created by Fernando Bermudez on 06/10/2019.
//  Edited by Fernando Bermudez and Gabriel Santiago on June 10, 2020
//  Edited by Gabriel Santiago on June 20, 2021
//  Edited by Orlando Saldaña on July 23, 2021
//  Copyright © 2020 bermedDev. All rights reserved.
//  Copyright © 2020 teamMADE. All rights reserved.
"""
import asyncio
from typing import Coroutine

import discord
from discord.app_commands import CommandTree

import config
import event_listeners
import log
from commands import subscribe_slash_commands
from controllers import daily_logs, eo_monitor, join_listener, leveling_system
from db import close_db
from event_listeners import profanity_filter

# Enable intents.
# Documentation: https://discordpy.readthedocs.io/en/latest/intents.html
enabled_intents: discord.Intents = discord.Intents.all()

enabled_intents.dm_messages = True
enabled_intents.guild_messages = True
enabled_intents.guilds = True
enabled_intents.members = True
enabled_intents.message_content = True
enabled_intents.messages = True
enabled_intents.reactions = True
enabled_intents.typing = True
enabled_intents.presences = True
enabled_intents.webhooks = True

client = discord.Client(intents=enabled_intents)

cmd_tree = CommandTree(client=client)


async def main():
    global client

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            # Events related to bot response
            return
        log.info(f"[on_message] {message}")

        has_profanity = await profanity_filter.on_message(message)
        if has_profanity:
            return

        log.info(f"[USER] {message.author.name}#{message.author.discriminator}")

        await leveling_system.on_message(message)
        await event_listeners.on_message(message, client)

        # Created event passed Message object
        # to use for response of bot to discord client
        daily_logs.analytics(message)

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        await profanity_filter.on_message(after)

    @client.event
    async def on_member_join(member: discord.Member):
        await join_listener.on_join(member, client)
        await eo_monitor.listeners.on_member_join(member)

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        await eo_monitor.listeners.on_member_update(before, after)

    @client.event
    async def on_ready():
        await client.wait_until_ready()
        await subscribe_slash_commands(cmd_tree)
        await cmd_tree.sync()
        await eo_monitor.listeners.on_ready(client)
        log.info("[VERBOSE] On Ready Finished.")

    # start the client
    async with client:
        await client.start(config.BOT_TOKEN)

    return 0


if __name__ == "__main__":
    coroutine: Coroutine = None
    try:
        coroutine = asyncio.run(main())
        if coroutine:
            coroutine.close()
    except KeyboardInterrupt:
        log.info("Program ended")
        if coroutine:
            coroutine.close()
    except Exception as error:
        log.error(f"Unexpected error {error}")
    finally:
        if coroutine:
            coroutine.close()
            log.error("[EXIT] Closed coroutine...")

        close_db()
