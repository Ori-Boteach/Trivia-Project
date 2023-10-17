"""
Author: Ori Boteach
File Name: server_test (pytest unnitesting for the server side)
Change Log: creation - 17/10/2023
"""
from unittest.mock import patch, Mock
from server import handle_getscore_message, messages_to_send, handle_highscore_message, handle_logged_message


@patch('server.users', {"test": {"score": 5}})
def test_handle_getscore_message():
    """
    test that the handle_getscore_message function and validate that it adds the correct message to the messages_to_send list
    :return: whether the expected message was added to the messages_to_send list
    """
    # Arrange
    username = "test"
    expected_message = "YOUR_SCORE      |0001|5"
    mock_socket = Mock()  # Create a mock socket

    # Act
    handle_getscore_message(mock_socket, username)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server.users', {"test": {"score": 0}, "master": {"score": 200}, "yossi": {"score": 50}})
def test_handle_highscore_message():
    """
    test the handle_highscore_message function and validate that it adds the correct message to the messages_to_send list
    :return: whether the expected message was added to the messages_to_send list
    """
    # Arrange
    expected_message = "ALL_SCORE       |0030|master: 200\nyossi: 50\ntest: 0\n"
    mock_socket = Mock()

    # Act
    handle_highscore_message(mock_socket)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server.logged_users', {("127.0.0.1", 52116): "test", ("127.0.0.1", 52117): "master"})
def test_handle_logged_message():
    """
    test the handle_logged_message function and validate that it adds the correct message to the messages_to_send list
    :return: whether the expected message was added to the messages_to_send list
    """
    # Arrange
    expected_message = "LOGGED_ANSWER   |0012|test, master"
    mock_socket = Mock()

    # Act
    handle_logged_message(mock_socket)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


# ------ handle_question_message ----------------------------


# ------ handle_answer_message ----------------------------


# ------ handle_client_message ----------------------------
