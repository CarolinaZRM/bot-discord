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
from event_handlers import (
    actions,
    actions2,
    attendance,
    channel,
    easter_eggs,
    fun_games,
    join,
    links,
    prepa,
    sanitize,
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

cm_tree = CommandTree(client=client)


async def main():
    global client

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            # Events related to bot response
            return

        log.debug(f"[INFO] [Func: on_message] MessageObj: {message}")

        adding_profanity = await sanitize.add_profanity_to_list(message)

        if adding_profanity:
            log.debug(f"[DEBUG] {message.author} added new profanity.")
            return

        has_profanity = await sanitize.profanity_filter(message)
        if has_profanity:
            log.debug("[DEBUG] Has profanity")
            return

        log.debug(f"[USER] {message.author.name}#{message.author.id}")
        if (
            message.content.startswith("!bulk_delete_admin")
            and bot.is_sender_admin(message)
            and not bot.is_from_dm(message)
        ):
            sections = message.content.split(":")
            log.debug(f"[DEBUG] DELETE COMMAND SECTIONS: {sections}")
            log.debug(f"[DEBUG] BULK DELETE FILTER PASSED BY ADMIN {message.author}")
            if len(sections) == 2 and sections[1].isdigit():
                deleted = await message.channel.purge(limit=int(sections[1]))
                log.debug(
                    f'[DEBUG] Deleted {len(deleted)} messages. " \
                    " Selected by user {message.author}'
                )
            else:
                while len(await message.channel.purge(limit=1500)) > 0:
                    log.debug(
                        f"[DEBUG DLT] BULK DELETE ' \
                            'CALLED BY ADMIN {message.author}"
                    )

        log.debug("[INFO] passed the filter")

        # Created event passed Message object
        # to use for response of bot to discord client
        daily_logs.analytics(message)

        await actions.event_get_curriculum(message)
        await actions.event_help_menu(message)
        await actions.event_parse_university_building(message)
        await actions.event_telephone_guide(message)
        await actions.generate_faq(message)
        await bot.general_leaderboard(message)
        await actions.get_prj_info(message)
        await attendance.subscribe_attendance(message)
        await easter_eggs.subscribe_easter_eggs(message)
        await fun_games.event_guessing_game(message, client)
        await fun_games.event_ping_pong(message)
        await fun_games.event_rock_paper_scissor(message, client)
        await links.event_links(message)
        await prepa.get_counselor_names(message)
        await bot.level_on_message(message)
        await bot.leveling_status(message)
        await bot.download_user_level_data(message)

        # On message action for leveling system

        if bot.is_sender_counselor(message):
            # commands for admins and student counselors
            log.debug("[DEBUG] Entered Counselor Auth Zone")
            await channel.event_user_count(message)
        elif bot.is_sender_prepa(message):
            # commands for prepas
            pass

        # await client.process_commands(message)

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
            log.debug(f"[DEBUG] before: {before} After: {after}")
            await bot.update_admin_list(client)
            prepa.extract_counselors(client)

    @client.event
    async def on_ready():
        await client.wait_until_ready()

        await actions2.subscribe_actions(command_tree=cm_tree)

        await cm_tree.sync()

        log.debug(f"[DEBUG] Guild Obj: {client.guilds}")
        await bot.update_admin_list(client)
        prepa.extract_counselors(client)
        log.debug("[VERBOSE] On Ready Finished.")

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
        log.debug("[DEBUG] Program ended")
        if coroutine:
            coroutine.close()
    except Exception as error:
        log.debug(f"[ERROR] Unexpected error {error}")
    finally:
        if coroutine:
            coroutine.close()
            log.debug("[EXIT] Closed coroutine...")
