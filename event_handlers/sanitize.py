# https://github.com/snguyenthanh/better_profanity
import better_profanity
import discord
import log


async def profanity_filter(message: discord.Message) -> None:
    """
    If message contains a profanity return `True`, else return `False`
    """
    if better_profanity.profanity.contains_profanity(message.content):
        user_message = message.content
        log.debug(f'Containes a bad word: {user_message}')
        author = None
        if hasattr(message.author, 'nick'):
            author = message.author.nick
        else:
            author = message.author.name
        await message.delete(delay=None)
        print(f"""{author} said a bad word, deleting message""")
        await message.channel.send(f"""{author} said a bad word, deleting message""")
        return True
    return False
