# https://github.com/snguyenthanh/better_profanity
from better_profanity import profanity
import discord
import log
import os

_CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))


def __init_sanitize():
    global _CURRENT_DIR
    log.debug('[VERBOSE] Initializing additional Spanish Profanities')

    file_path = os.path.join(
        _CURRENT_DIR, "res", "textfiles", "spanish_profanities.txt")
    censored_spanish_words = open(file_path, 'r')

    lines = censored_spanish_words.readlines()
    censored_spanish_words.close()
    lines = list(map(lambda x: x.strip().lower(), lines))

    combinations = set()
    for word in lines:
        num_of_non_allowed_chars = profanity._count_non_allowed_characters(
            word)
        if num_of_non_allowed_chars > profanity.MAX_NUMBER_COMBINATIONS:
            profanity.MAX_NUMBER_COMBINATIONS = num_of_non_allowed_chars

        combinations.update(
            set(profanity._generate_patterns_from_word(word)))

    profanity.add_censor_words(combinations)
    print(combinations)
    log.debug('[VERBOSE] Finished adding additional Spanish Profanities')


__init_sanitize()


async def profanity_filter(message: discord.Message) -> None:
    """
    If message contains a profanity return `True`, else return `False`
    """
    user_message = message.content
    if _profanity_filter.is_profane(user_message) or profanity.contains_profanity(user_message):
        # if better_profanity.profanity.contains_profanity(message.content):
        channel_sent = message.channel
        log.debug(f'Containes a bad word: {user_message}')
        author = None
        if hasattr(message.author, 'nick'):
            author = message.author.nick
        else:
            author = message.author.name
        await message.delete(delay=0)
        print(f"""{author} dijo una profanidad, borré el mensaje""")
        await channel_sent.send(f"""{author} dijo una profanidad, borré el mensaje""")
        return True
    return False
