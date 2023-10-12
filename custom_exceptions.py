"""
Author: Ori Boteach
File Name: custom_exceptions
Change Log: creation - 12/10/2023
"""


class NoneExistingProtocol:
    """ a custom exception for a protocol command that does not exist"""

    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return f"the provided command: {self.cmd}, does not exist!"


class InvalidFieldLength:
    """ a custom exception for a field that exceeds max length"""

    def __str__(self):
        return "one of the fields' length in the protocol is over the limit"


class InvalidLengthField:
    """ a custom exception for a length field that does not consist of only digits or spaces"""

    def __str__(self):
        return "the length field does not consist of only digits or spaces"


class InvalidDelimiterCount:
    """ a custom exception for a number of delimiters in the message other than two"""

    def __init__(self, count):
        self.count = count

    def __str__(self):
        return f"there are {self.count} delimiters in the whole field but there should be 2!"
