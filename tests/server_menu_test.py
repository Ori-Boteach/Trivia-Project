"""
Author: Ori Boteach
File Name: server_test (pytest unnitesting for the server side)
Change Log: creation - 17/10/2023
"""
from unittest.mock import patch, Mock
from constants import PROTOCOL_CLIENT
from server import handle_client_message
from server_helpers import messages_to_send
from server_menu_handlers import handle_getscore_message, handle_highscore_message, handle_logged_message


@patch('server_menu_handlers.users', {"test": {"score": 5}})
def test_handle_getscore_message():
    """
    test that the handle_getscore_message function and validate
    that it adds the correct message to the messages_to_send list
    :return: whether the expected message was added to the messages_to_send list
    """
    # Arrange
    username = "test"
    expected_message = "YOUR_SCORE      |0001|5"
    mock_socket = Mock()  # create a mock socket

    # Act
    handle_getscore_message(mock_socket, username)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server_menu_handlers.users', {"test": {"score": 0}, "master": {"score": 200}, "yossi": {"score": 50}})
def test_handle_highscore_message():
    """
    test the handle_highscore_message function and validate
    that it adds the correct message to the messages_to_send list
    :return: whether the expected message was added to the messages_to_send list
    """
    # Arrange
    expected_message = "ALL_SCORE       |0030|master: 200\nyossi: 50\ntest: 0\n"
    mock_socket = Mock()

    # Act
    handle_highscore_message(mock_socket)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server_menu_handlers.logged_users', {("127.0.0.1", 52116): "test", ("127.0.0.1", 52117): "master"})
def test_handle_logged_message():
    """
    test the handle_logged_message function and validate
    that it adds the correct message to the messages_to_send list
    :return: whether the expected message was added to the messages_to_send list
    """
    # Arrange
    expected_message = "LOGGED_ANSWER   |0012|test, master"
    mock_socket = Mock()

    # Act
    handle_logged_message(mock_socket)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server.handle_login_message')
@patch('server_menu_handlers.logged_users', {("127.0.0.1", 52116): "test", ("127.0.0.1", 52117): "master"})
def test_handle_client_not_logged_user_command(mock_logout):
    """
    test the handle_client_message function for a not logged user command and check
    that it calls the handle_login_message function if needed
    :param mock_logout: a mock logout function
    """
    # Arrange
    mock_socket = Mock()
    cmd = PROTOCOL_CLIENT["login_msg"]
    data = "not logged in user#password"

    # configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("not logged in user", 52116)

    # Act
    handle_client_message(mock_socket, cmd, data)

    # Assert that the handle_logout_message function is called
    mock_logout.assert_called_once_with(mock_socket, "LOGIN           |0027|not logged in user#password")


@patch('server.handle_getscore_message')
@patch('server_menu_handlers.logged_users', {("127.0.0.1", 52116): "test", ("127.0.0.1", 52117): "master"})
def test_handle_client_logged_user_command(mock_login):
    """
    test the handle_client_message function for a logged user command and check
    that one of the possible commands is actually being called
    :param mock_login: a mock handle_getscore_message function
    """
    # Arrange
    mock_socket = Mock()
    cmd = PROTOCOL_CLIENT["my_score_msg"]
    data = "example data"

    # configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("127.0.0.1", 52116)

    # Act
    handle_client_message(mock_socket, cmd, data)

    # Assert that the handle_login_message function is called
    mock_login.assert_called_once_with(mock_socket, "test")


@patch('server.send_error')
def test_handle_client_unknown_command(mock_send_error):
    """
    test the handle_client_message function for an unknown command and check
    that the send_error function is being called
    :param mock_send_error: a mock send_error function
    """
    # Arrange
    mock_socket = Mock()
    cmd = "unknown_command"
    data = "some data"

    # Act
    handle_client_message(mock_socket, cmd, data)

    # Assert that send_error function is called with the correct error message
    mock_send_error.assert_called_once_with(mock_socket, "command is not recognized!")
