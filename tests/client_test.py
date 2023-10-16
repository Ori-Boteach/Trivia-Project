"""
Author: Ori Boteach
File Name: client_test (pytest unnitesting for the client side)
Change Log: creation - 16/10/2023
"""

import socket
from unittest.mock import patch
from client import get_score, get_highscore, get_logged_users, play_question
from client_helpers import logout
from constants import PROTOCOL_SERVER


@patch('client.build_send_recv_parse')
def test_get_score(mock_build_send_recv_parse, capsys):
    """
    Test the get_score function and validate that it prints the correct score
    :param mock_build_send_recv_parse: a mock function that replaces build_send_recv_parse
    :param capsys: a pytest fixture that captures printed output
    """
    # Arrange
    # Configure the mock function to return the expected data
    mock_build_send_recv_parse.return_value = (PROTOCOL_SERVER["your_score_msg"], "5")
    # Create a mock socket
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Act (call the function with the mock socket)
    get_score(mock_socket)

    # Assert (validate that the function printed the correct score)
    assert capsys.readouterr().out == "Your score is: 5\n"


@patch('client.build_send_recv_parse')
def test_get_high_score(mock_build_send_recv_parse, capsys):
    """
    Test the get_highscore function and validate that it prints the correct scores list
    :param mock_build_send_recv_parse: a mock function that replaces build_send_recv_parse
    :param capsys: a pytest fixture that captures printed output
    """
    # Arrange
    # Configure the mock function to return the expected data
    mock_build_send_recv_parse.return_value = (PROTOCOL_SERVER["all_score_msg"], "master: 200\nyossi: 50\ntest: 0")
    # Create a mock socket
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Act (call the function with the mock socket)
    get_highscore(mock_socket)

    # Assert (validate that the function printed the correct score)
    assert capsys.readouterr().out == "high scores:\nmaster: 200\nyossi: 50\ntest: 0\n"


@patch('client.build_send_recv_parse')
def test_get_logged_users(mock_build_send_recv_parse, capsys):
    """
    Test the get_logged_users function and validate that it prints the correct users list
    :param mock_build_send_recv_parse: a mock function that replaces build_send_recv_parse
    :param capsys: a pytest fixture that captures printed output
    """
    # Arrange
    # Configure the mock function to return the expected data
    mock_build_send_recv_parse.return_value = (PROTOCOL_SERVER["logged_answer_msg"], "test, master")
    # Create a mock socket
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Act (call the function with the mock socket)
    get_logged_users(mock_socket)

    # Assert (validate that the function printed the correct score)
    assert capsys.readouterr().out == "logged users:\ntest, master\n"


@patch('builtins.input', side_effect=['2'])
@patch('client.build_send_recv_parse')
def test_play_right_answer(mock_build_send_recv_parse, capsys):
    """
    Test the play_question function and validate the response to the user is correct
    :param mock_build_send_recv_parse: a mock function that replaces build_send_recv_parse
    :param capsys: a pytest fixture that captures inputted output
    """
    # Arrange
    # Configure the mock function to return the expected data
    mock_build_send_recv_parse.side_effect = [
        (PROTOCOL_SERVER["your_question_msg"], "2313#How much is 2+2#3#4#2#1"),
        (PROTOCOL_SERVER["correct_answer_msg"], "")
    ]
    # Create a mock socket
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Act (call the function with the mock socket)
    answer_result = play_question(mock_socket)

    # Assert (validate that the function printed the correct score)
    assert answer_result is True


@patch('builtins.input', side_effect=['1'])
@patch('client.build_send_recv_parse')
def test_play_wrong_answer(mock_build_send_recv_parse, capsys):
    """
    Test the play_question function and validate the response to the user is correct
    :param mock_build_send_recv_parse: a mock function that replaces build_send_recv_parse
    :param capsys: a pytest fixture that captures inputted output
    """
    # Arrange
    # Configure the mock function to return the expected data
    mock_build_send_recv_parse.side_effect = [
        (PROTOCOL_SERVER["your_question_msg"], "2313#How much is 2+2#3#4#2#1"),
        (PROTOCOL_SERVER["wrong_answer_msg"], "")
    ]
    # Create a mock socket
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Act (call the function with the mock socket)
    answer_result = play_question(mock_socket)

    # Assert (validate that the function printed the correct score)
    assert answer_result is False


@patch('client_helpers.build_and_send_message')
def test_logout(mock_build_send_recv_parse, capsys):
    """
    Test the logout function and validate that the correct response is printed
    :param mock_build_send_recv_parse: a mock function that replaces build_send_recv_parse
    :param capsys: a pytest fixture that captures printed output
    """
    # Arrange (create a mock socket)
    mock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Act (call the function with the mock socket)
    logout(mock_socket)

    # Assert (validate that the function printed the correct score)
    assert capsys.readouterr().out == "Goodbye!\n"
