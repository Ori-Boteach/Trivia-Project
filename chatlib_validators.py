"""
Author: Ori Boteach
File Name: validators
Change Log: creation - 12/10/2023
"""

from constants import *
from custom_exceptions import NoneExistingProtocol, InvalidFieldLength, InvalidDelimiterCount, InvalidLengthField


def build_validator(cmd: str, data: str) -> None:
    """
    the function performs validations for the build function (length and valid command)
    :param cmd: the inputted command field
    :param data: the whole inputted protocol data
    :raise: InvalidFieldLength if the fields lengths are incorrect
    :raise: NoneExistingProtocol if the command doesn't exist
    """
    if len(data) > MAX_DATA_LENGTH or len(cmd) > CMD_FIELD_LENGTH:
        raise InvalidFieldLength

    if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
        raise NoneExistingProtocol(cmd)


def initial_parser_validator(data: str) -> None:
    """
    the function performs initial validations on the given data (delimiter count and length)
    :param data: the whole inputted protocol data
    :raise: InvalidDelimiterCount if the delimiter count is not two
    :raise: InvalidFieldLength if the data length is incorrect
    """
    if data.count(DELIMITER) != 2:
        raise InvalidDelimiterCount(data.count(DELIMITER))

    if len(data) > MAX_MSG_LENGTH:
        raise InvalidFieldLength


def parser_fields_validator(cmd: str, length: str, message: str) -> None:
    """
    the function performs more validations on the inputted data (lengths, valid command and length fields)
    :param cmd: the inputted command field
    :param length: the inputted length field
    :param message: the inputted message field
    :raise: InvalidFieldLength if the fields lengths are incorrect
    :raise: NoneExistingProtocol if the command doesn't exist
    :raise: InvalidLengthField if the length field isn't numeric
    """
    # validate fields lengths
    if len(cmd) != CMD_FIELD_LENGTH or len(length) != LENGTH_FIELD_LENGTH or len(message) > MAX_DATA_LENGTH:
        raise InvalidFieldLength

    # check that the given command is valid
    cmd = cmd.replace(" ", "")
    if cmd not in PROTOCOL_CLIENT.values() and cmd not in PROTOCOL_SERVER.values():
        raise NoneExistingProtocol(cmd)

    # can work both with spaces and with zeros!
    length = length.replace(" ", "0")
    if not length.isnumeric():
        raise InvalidLengthField
