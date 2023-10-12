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
    Returns: str, or None if error occured
    """

    # validate inputs
    if len(data) > MAX_DATA_LENGTH or len(cmd) > CMD_FIELD_LENGTH:
        return ERROR_RETURN

    if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
        return ERROR_RETURN

    # CHECK FOR INVALID DATA??

    # calculate return message
    string_len = str(len(data))
    msg_length = string_len.rjust(LENGTH_FIELD_LENGTH, '0')

    padded_cmd = cmd.ljust(CMD_FIELD_LENGTH, " ")

    full_msg = padded_cmd + DELIMITER + msg_length + DELIMITER + data
    return full_msg


def parse_message(data: str):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
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

    # VALIDATE MESSAGE ??

    return cmd, message


def split_data(msg: str, expected_fields: int) -> List:
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """

    if msg.count(DATA_DELIMITER) == expected_fields:
        fields_list = msg.split(DATA_DELIMITER)
        return fields_list

    return [ERROR_RETURN]


def join_data(msg_fields: List[str]) -> str:
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    return "#".join(msg_fields)
