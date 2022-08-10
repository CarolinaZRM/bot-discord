"""
//  /bot-discord/commands/server_management/bulk_delete_admin.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/09
//  
//  Last Modified: Tuesday, 9th August 2022 10:37:24 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

from typing import Union

import log
from discord import Interaction, Member, User
from discord.app_commands import Command, checks


def command():
    cmd = Command(
        name="bulk_delete_admin",
        description="Delete messages in bulk.",
        callback=_bulk_delete_admin,
    )

    return cmd


@checks.has_role("Administrator")
async def _bulk_delete_admin(interaction: Interaction, messages_to_delete: int):
    author: Union[Member, User] = interaction.user
    log.info(f"[USER] {author.display_name} #{author.id}")

    if isinstance(author, User):
        log.info(f"Comes from DM {author}")
        await interaction.response.send_message(
            "No puedes hacer bulk delete desde un DM. Intenta desde un 'channel' dentro del Server"
        )
        return

    # sections = message.content.split(":")
    log.info(f"BULK DELETE FILTER PASSED BY ADMIN {author}")

    if messages_to_delete:
        deleted = await interaction.channel.purge(
            limit=messages_to_delete,
        )
        log.info(f"Deleted {len(deleted)} messages.  Selected by user {author}")
    else:
        while len(await interaction.channel.purge(limit=1500)) > 0:
            log.info(f"BULK DELETE CALLED BY ADMIN {author}")

    await interaction.response.defer(thinking=False)
