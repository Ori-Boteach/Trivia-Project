"""
Author: Ori Boteach
File Name: server_logging_test (pytest unnitesting for the server side)
Change Log: creation - 17/10/2023
"""
from unittest.mock import Mock, patch
from server import handle_logout_message, handle_login_message, logged_users
from server_helpers import messages_to_send


@patch('server.logged_users', {("127.0.0.1", 52116): "test", ("127.0.0.1", 52117): "master"})
def test_handle_logout_message():
    """
    test the handle_logout_message function and validate that it removes the user from the logged_users dictionary
    :return: true if the logged-out user was removed from the logged_users dictionary
    """
    # Arrange
    mock_socket = Mock()

    # Configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("127.0.0.1", 52116)

    # Act
    handle_logout_message(mock_socket)

    # Access the patched dictionary using the mock object
    patched_logged_users = patch('server.logged_users').get_original()

    # Assert (check if the user is removed from the logged_users dictionary)
    assert ("127.0.0.1", 52116) not in patched_logged_users


@patch('server.users', {"test": {"password": "test", "score": 0, "questions_asked": []}})
def test_successful_login():
    """
    test the handle_login_message function and validate that it adds the user to the logged_users dictionary
    :return: true if the new user was added to the logged_users dictionary
    """
    # Arrange
    mock_socket = Mock()
    client_sent_data = "LOGIN           |0009|test#test"

    # Configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("127.0.0.1", 52117)

    # Act
    handle_login_message(mock_socket, client_sent_data)

    # Assert (check if the user is added to the logged_users dictionary)
    assert ("127.0.0.1", 52117) in logged_users


@patch('server.users', {"test": {"password": "test", "score": 0, "questions_asked": []}})
def test_wrong_username_login():
    """
    test the handle_login_message function and validate that it does not add a user
    with a wrong username to the logged_users dictionary
    :return: true if the incorrect user was not added to the logged_users dictionary
    """
    # Arrange
    mock_socket = Mock()
    client_sent_data = "LOGIN           |0026|none_existing_username#123"
    expected_message = "ERROR           |0032|Error! Username does not exists!"

    # Configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("127.0.0.1", 52117)

    # Act
    handle_login_message(mock_socket, client_sent_data)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server.users', {"test": {"password": "test", "score": 0, "questions_asked": []}})
def test_wrong_password_login():
    """
    test the handle_login_message function and validate that it does not add a user
    with a wrong password to the logged_users dictionary
    :return: true if the new user was added to the logged_users dictionary
    """
    # Arrange
    mock_socket = Mock()
    client_sent_data = "LOGIN           |0019|test#wrong_password"
    expected_message = "ERROR           |0031|Error! Password does not match!"

    # Configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("127.0.0.1", 52117)

    # Act
    handle_login_message(mock_socket, client_sent_data)

    # Assert (check if the message is in the messages_to_send list)
    assert (mock_socket, expected_message.encode()) in messages_to_send
