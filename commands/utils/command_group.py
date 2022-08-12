"""
// /bot-discord/commands/utils/command_group.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/11
//  
//  Last Modified: Thursday, 11th August 2022 4:40:06 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""

from typing import Any, Callable, Coroutine
from discord.app_commands import Group

from discord import Interaction

__all__ = ["InteractionCheckedGroup"]


class InteractionCheckedGroup(Group):
    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.interaction_checker:
            return await self.interaction_checker(interaction)
        return True

    def set_interaction_check(
        self,
        interaction_checker: Callable[[Interaction], Coroutine[Any, Any, bool]],
    ) -> None:
        self.interaction_checker = interaction_checker
