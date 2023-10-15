"""
Author: Ori Boteach
File Name: chatlib
Change Log: creation - 12/10/2023
"""

from typing import List

from constants import *
from validators import build_validator, initial_parser_validator, parser_fields_validator


def build_message(cmd: str, data: str) -> str:
    """
    Gets command name (str) and message field (str) and creates a valid protocol message
    :param cmd: the command name
    :param data: the message field
    :return: str of the full message, or None if error occurred
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


def parse_message(data: str):
    """
    Parses protocol message and returns command name and data field
    :param data: a full inputted message
    :return: cmd (str), data (str). If some error occurred, returns None, None
    """

    # validate delimiter count and whole data length
    try:
        initial_parser_validator(data)
    # using broad exception like taught because acting the same for all caught exceptions
    except Exception:
        return ERROR_RETURN, ERROR_RETURN

    # separating the data to it's fields
    subfields = data.split(DELIMITER)

    cmd = subfields[0]
    length = subfields[1]
    message = subfields[2]

    # validate field's lengths and contents
    try:
        parser_fields_validator(cmd, length, message)
    # using broad exception like taught because acting the same for all caught exceptions
    except Exception:
        return ERROR_RETURN, ERROR_RETURN

    # remove padding spaces from the command field
    cmd = cmd.replace(" ", "")

    return cmd, message


def split_data(msg: str, expected_delimiters: int) -> List[str]:
    """
    Helper method. gets a string and number of expected delimiters in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    :param msg: the message field
    :param expected_delimiters: number of expected delimiters in it
    :return: list of fields if all ok. If some error occurred, returns None
    """

    if msg.count(DATA_DELIMITER) == expected_delimiters:
        return msg.split(DATA_DELIMITER)

    return [ERROR_RETURN]


def join_data(msg_fields: List[str]) -> str:
    """
    Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
    :param msg_fields: a list representing subfields in the message field
    :return: string that looks like cell1#cell2#cell3
    """
    return "#".join(msg_fields)
