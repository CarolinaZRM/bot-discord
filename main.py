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
from calendar import c
from datetime import datetime
from typing import Coroutine

import discord
from discord.app_commands import CommandTree
from discord.ext.commands import Bot, Context

import bot

import config
import log
from commands import (
    actions,
    easter_eggs,
    fun_games,
    join,
    prepa,
    sanitize,
    subscribe_slash_commands,
)

from controllers import daily_logs

# Enable intents.
# Documentation: https://discordpy.readthedocs.io/en/latest/intents.html
enabled_intents: discord.Intents = discord.Intents.all()

enabled_intents.dm_messages = True
enabled_intents.guilds = True
enabled_intents.members = True
enabled_intents.messages = True
enabled_intents.reactions = True
enabled_intents.typing = True
enabled_intents.presences = True
enabled_intents.message_content = True
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

        log.info(f"[Func: on_message] MessageObj: {message}")

        adding_profanity = await sanitize.add_profanity_to_list(message)

        if adding_profanity:
            log.info(f"{message.author} added new profanity.")
            return

        has_profanity = await sanitize.profanity_filter(message)
        if has_profanity:
            log.info("Has profanity")
            return

        log.info(f"[USER] {message.author.name}#{message.author.id}")
        if (
            message.content.startswith("!bulk_delete_admin")
            and bot.is_sender_admin(message)
            and not bot.is_from_dm(message)
        ):
            sections = message.content.split(":")
            log.info(f"DELETE COMMAND SECTIONS: {sections}")
            log.info(f"BULK DELETE FILTER PASSED BY ADMIN {message.author}")
            if len(sections) == 2 and sections[1].isdigit():
                deleted = await message.channel.purge(limit=int(sections[1]))
                log.info(
                    f'Deleted {len(deleted)} messages. " \
                    " Selected by user {message.author}'
                )
            else:
                while len(await message.channel.purge(limit=1500)) > 0:
                    log.info(
                        f"BULK DELETE ' \
                            'CALLED BY ADMIN {message.author}"
                    )

        log.info("passed the filter")

        # Created event passed Message object
        # to use for response of bot to discord client
        daily_logs.analytics(message)

        await actions.event_get_curriculum(message)
        await actions.event_parse_university_building(message)
        await actions.get_made_website(message)
        await actions.get_prj_info(message)
        await bot.download_user_level_data(message)
        await bot.general_leaderboard(message)
        await bot.level_on_message(message)
        await bot.leveling_status(message)
        await easter_eggs.subscribe_easter_eggs(message)
        await fun_games.event_guessing_game(message, client)
        await fun_games.event_ping_pong(message)
        await fun_games.event_rock_paper_scissor(message, client)
        await prepa.get_counselor_names(message)

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        _ = await sanitize.profanity_filter(after)

    @client.event
    async def on_member_join(member: discord.Member):
        await bot.verify_if_counselor(member)
        await join.event_greet_new_member(client, member)
        await join.made(member)
        await bot.level_join(member)

    @client.event
    async def on_member_update(before, after):
        if before.roles != after.roles:
            log.info(f"before: {before} After: {after}")
            await bot.update_admin_list(client)
            prepa.extract_counselors(client)

    @client.event
    async def on_ready():
        await client.wait_until_ready()

        await subscribe_slash_commands(cmd_tree)
        await cmd_tree.sync()

        log.info(f"Guild Obj: {client.guilds}")
        await bot.update_admin_list(client)
        prepa.extract_counselors(client)

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
