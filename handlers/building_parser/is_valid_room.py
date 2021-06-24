import re


def is_valid_room_number(sections):
    if len(sections) == 1:
        return False

    tmp = sections[1]

    regex_result = re.findall("^\D+", tmp)

    if len(regex_result) == 1:
        return True

    return False
