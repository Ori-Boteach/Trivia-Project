"""
Author: Ori Boteach
File Name: chatlib
Change Log: creation - 12/10/2023
"""

from constants import *
from chatlib_validators import build_validator, initial_parser_validator, parser_fields_validator


def build_message(cmd: str, data: str) -> str:
    """
    the function gets command name and message field and creates a valid protocol message
    :param cmd: the command name
    :param data: the message field
    :return: str of the full message, or None if error occurred
    :except: ERROR_RETURN if InvalidFieldLength or NoneExistingProtocol errors occurred
    """

    # validating inputs
    try:
        build_validator(cmd, data)

    # using broad exception like taught because acting the same for all caught exceptions
    except Exception:
        return ERROR_RETURN

    # calculate return message
    string_len = str(len(data))
    msg_length = string_len.rjust(LENGTH_FIELD_LENGTH, '0')

    padded_cmd = cmd.ljust(CMD_FIELD_LENGTH, " ")

    full_msg = padded_cmd + DELIMITER + msg_length + DELIMITER + data
    return full_msg


def parse_message(data: str) -> tuple[str, str]:
    """
    the function parses protocol message and returns command name and data field
    :param data: a full inputted message
    :return: cmd and data. If some error occurred, returns None, None
    :except: ERROR_RETURN, ERROR_RETURN if InvalidDelimiterCount or InvalidFieldLength errors occurred
    :except: ERROR_RETURN, ERROR_RETURN if InvalidFieldLength, NoneExistingProtocol or InvalidLengthField errors
    """

    # validate delimiter count and whole data length
    try:
        initial_parser_validator(data)
    # using broad exception like taught because acting the same for all caught exceptions
    except Exception:
        return ERROR_RETURN, ERROR_RETURN

    # separating the data to it's fields
    subfields = data.split(DELIMITER)

    cmd, length, message = subfields

    # validate field's lengths and contents
    try:
        parser_fields_validator(cmd, length, message)
    # using broad exception like taught because acting the same for all caught exceptions
    except Exception:
        return ERROR_RETURN, ERROR_RETURN

    # remove padding spaces from the command field
    cmd = cmd.replace(" ", "")

    return cmd, message


def split_data(msg: str, expected_delimiters: int) -> list[str]:
    """
    the function is a helper method. It gets a string of the message field and number of expected delimiters in it.
    Splits the string using the message field delimiter (#) and validates that there are correct number of fields
    :param msg: the message field
    :param expected_delimiters: number of expected delimiters in it
    :return: a list of fields in message if all ok. if delimiter count is different, returns None
    """

    # validate number of delimiters is as expected
    if msg.count(DATA_DELIMITER) == expected_delimiters:
        return msg.split(DATA_DELIMITER)

    return [ERROR_RETURN]


def join_data(msg_fields: list[str]) -> str:
    """
    the function is a helper method. It gets a list, joins all of its fields to one string divided by the data delimiter
    :param msg_fields: a list representing subfields in the message field
    :return: a string representing the whole message field. If length is too long, returns None
    """
    message_field = DATA_DELIMITER.join(msg_fields)

    # validate message field length doesnt exceed maximum
    if len(message_field) > MAX_DATA_LENGTH:
        return ERROR_RETURN

    return message_field
