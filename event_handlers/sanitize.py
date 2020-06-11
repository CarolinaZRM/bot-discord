import better_profanity
import discord
import log


async def profanity_filter(message: discord.Message) -> None:
    """
    If message contains a profanity return `True`, else return `False`
    """
    user_message = message.content
    bad_words = ["cabron", "cabrona", "mamabicho", "puta", "puto", "pendejo", "pendeja",
                 "fuck", "shit", "motherfucker", "bellaco", "bellaca", "wlb", "bicho", "cb", "beber"]

    sanitized = user_message.replace(',', '').replace(
        ' ', '').replace('-', '').lower()
    log.debug(f'Sanitized String: {sanitized}')

    for bad_word in bad_words:
        if bad_word in sanitized:
            log.debug(f'Containes a bad word: {user_message}')

            author = None
            if hasattr(message.author, 'nick'):
                author = message.author.nick
            else:
                author = message.author.name

            await message.channel.purge(limit=1)
            print(f"""{author} said a bad word, deleting message""")
            await message.channel.send(f"""{author} said a bad word, deleting message""")

            return False
    return True
