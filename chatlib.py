"""
Author: Ori Boteach
File Name: chatlib
Change Log: creation - 12/10/2023
"""

from typing import List

from constants import *


def build_message(cmd: str, data: str) -> str:
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    :param cmd: the command name
    :param data: the data field
    :return: str of the full message, or None if error occurred
    """

    # validate inputs
    if len(data) > MAX_DATA_LENGTH or len(cmd) > CMD_FIELD_LENGTH:
        return ERROR_RETURN

    if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
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
    if data.count(DELIMITER) != 2 or len(data) > MAX_MSG_LENGTH:
        return ERROR_RETURN, ERROR_RETURN

    substrings = data.split(DELIMITER)

    cmd = substrings[0]
    length = substrings[1]
    message = substrings[2]

    # validate fields lengths
    if len(cmd) != CMD_FIELD_LENGTH or len(length) != LENGTH_FIELD_LENGTH or len(message) > MAX_DATA_LENGTH:
        return ERROR_RETURN, ERROR_RETURN

    # check that the given command is valid
    cmd = cmd.replace(" ", "")
    if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
        return ERROR_RETURN, ERROR_RETURN

    # can work both with spaces and with zeros!
    length = length.replace(" ", "0")
    if not length.isnumeric():
        return ERROR_RETURN, ERROR_RETURN

    # todo: VALIDATE MESSAGE ?

    return cmd, message


def split_data(msg: str, expected_fields: int) -> List[str]:
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    :param msg: the message field
    :param expected_fields: number of expected fields in it
    :return: list of fields if all ok. If some error occurred, returns None
    """

    if msg.count(DATA_DELIMITER) == expected_fields:
        return msg.split(DATA_DELIMITER)

    return [ERROR_RETURN]


def join_data(msg_fields: List[str]) -> str:
    """
    Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
    :param msg_fields: a list representing subfields in the message field
    :return: string that looks like cell1#cell2#cell3
    """
    return "#".join(msg_fields)
