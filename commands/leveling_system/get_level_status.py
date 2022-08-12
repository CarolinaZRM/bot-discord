"""
// /bot-discord/commands/leveling_system/get_level_status.py
//  py-bot-uprm
//  
//  Created by Gabriel S Santiago on 2022/08/11
//  
//  Last Modified: Thursday, 11th August 2022 8:01:12 pm
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//  
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.
"""
from typing import Dict, Union
from discord import Interaction, Embed
from discord.app_commands import Command

from controllers.leveling_system import get_level_info

LEVEL_ICONS = {
    1: "https://www.herald.wales/wp-content/uploads/2021/03/millenium-falcon-pembroke.jpg",
    2: "https://img1.cgtrader.com/items/3028889/de49dc859a/large/star-wars-jedi-starfighter-anakin-skywalker-3d-model-low-poly-animated-max.jpg",
    3: "https://s3-us-west-2.amazonaws.com/media.brothers-brick.com/2022/05/TieFighter-FukuSaku.jpg",
    4: "https://c-3d.niceshops.com/upload/image/product/large/default/revell-model-set-imperial-star-destroyer-1-pc-311143-en.jpg",
    5: "https://static.wikia.nocookie.net/starwars/images/7/74/AnakinsEta2.jpg/revision/latest?cb=20090424014352",
    6: "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/05/TIE-Fighter-Facts-Interceptor.jpg?q=50&fit=crop&w=963&h=481&dpr=1.5",
    7: "https://airandspace.si.edu/sites/default/files/styles/body_medium/public/2021-05/Composite_X-wing.jpg?itok=UwDAgRfB",
    8: "https://static.wikia.nocookie.net/starwars/images/c/c2/TIE_Defender.png/revision/latest?cb=20150801171146",
    9: "https://static.wikia.nocookie.net/starwars/images/6/66/Nimbus-class_V-wing_TFOWM.png/revision/latest?cb=20190629212809",
    10: "https://static.wikia.nocookie.net/starwars/images/a/af/Shuttle-CHRON.jpg/revision/latest?cb=20100813150543",
}


def command():
    return Command(name="my-level", description="See", callback=_get_level_status)


async def _get_level_status(interaction: Interaction):
    user = interaction.user

    user_level_info: Union[Dict[str, str], None] = get_level_info(user.id)
    if not user_level_info:
        return

    user_level = user_level_info.get("level", 1)
    image_url = LEVEL_ICONS.get(user_level) or LEVEL_ICONS.get(10)

    embed = Embed(
        title=f'Character Status: {getattr(user, "nick", user.name)}',
        description="Status of you character in the Team Made Leveling System",
        color=11901259,
    )
    embed.add_field(name="Level", value=user_level, inline=True)
    embed.add_field(
        name="Experience", value=user_level_info.get("experience", "N/A"), inline=True
    )
    embed.add_field(
        name="Number of Messages",
        value=user_level_info.get("messages", "N/A"),
        inline=True,
    )
    embed.set_image(url=image_url)

    await interaction.response.send_message(embed=embed)
