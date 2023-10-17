"""
Author: Ori Boteach
File Name: chatlib_test
Change Log: creation - 12/10/2023
"""
import chatlib


def test_build_normal_message():
    """ the function tests the build_message function with a normal input"""
    # Arrange
    input_cmd = "LOGIN"
    input_data = "aaaa#bbbb"
    expected_output = "LOGIN           |0009|aaaa#bbbb"

    # Act
    actual_output = chatlib.build_message(input_cmd, input_data)

    # Assert
    assert actual_output == expected_output


def test_build_empty_message():
    """ the function tests the build_message function with an empty input"""
    # Arrange
    input_cmd = "LOGIN"
    input_data = ""
    expected_output = "LOGIN           |0000|"

    # Act
    actual_output = chatlib.build_message(input_cmd, input_data)

    # Assert
    assert actual_output == expected_output


def test_build_too_long_cmd():
    """ the function tests the build_message function with a too long cmd"""
    # Arrange
    input_cmd = "0123456789ABCDEFG"
    input_data = ""
    expected_output = None

    # Act
    actual_output = chatlib.build_message(input_cmd, input_data)

    # Assert
    assert actual_output == expected_output


def test_build_too_long_message():
    """ the function tests the build_message function with a too long message"""
    # Arrange
    input_cmd = "A"
    input_data = "A" * (chatlib.MAX_DATA_LENGTH + 1)
    expected_output = None

    # Act
    actual_output = chatlib.build_message(input_cmd, input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_valid():
    """ the function tests the parse_message function with a valid input"""
    # Arrange
    input_data = "LOGIN           |   9|aaaa#bbbb"
    expected_output = ("LOGIN", "aaaa#bbbb")

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_valid_cmd():
    """ the function tests the parse_message function with a valid cmd"""
    # Arrange
    input_data = "           LOGIN|   9|aaaa#bbbb"
    expected_output = ("LOGIN", "aaaa#bbbb")

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_valid_length():
    """ the function tests the parse_message function with a valid length field"""
    # Arrange
    input_data = "LOGIN           |9   | aaa#bbbb"
    expected_output = ("LOGIN", " aaa#bbbb")

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_valid_delimiters():
    """ the function tests the parse_message function with no message delimiters"""
    # Arrange
    input_data = "LOGIN           |   4|data"
    expected_output = ("LOGIN", "data")

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_valid_zero_in_len():
    """ the function tests the parse_message function with a zero in the length field"""
    # Arrange
    input_data = "LOGIN           |  09|aaaa#bbbb"
    expected_output = ("LOGIN", "aaaa#bbbb")

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_invalid_delimiter():
    """ the function tests the parse_message function with an invalid delimiter"""
    # Arrange
    input_data = "LOGIN           x	  4|data"
    expected_output = (None, None)

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_empty_data():
    """ the function tests the parse_message function with an empty data """
    # Arrange
    input_data = ""
    expected_output = (None, None)

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_negative_length():
    """ the function tests the parse_message function with a negative length """
    # Arrange
    input_data = "LOGIN           |	 -4|data"
    expected_output = (None, None)

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_char_in_length():
    """ the function tests the parse_message function with a char in the length field """
    # Arrange
    input_data = "LOGIN           |	  z|data"
    expected_output = (None, None)

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output


def test_parse_invalid_length():
    """ the function tests the parse_message function with a too long length field """
    # Arrange
    input_data = "LOGIN           |	  5|data"
    expected_output = (None, None)

    # Act
    actual_output = chatlib.parse_message(input_data)

    # Assert
    assert actual_output == expected_output
